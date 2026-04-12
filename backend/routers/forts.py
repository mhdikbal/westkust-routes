from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import BaseModel, ConfigDict

from database import get_db
from models import Fort, Voyage

router = APIRouter()


# ---------- Schemas ----------

class FortBase(BaseModel):
    name: str
    latitude: float
    longitude: float
    color: str
    description: Optional[str] = None
    port_type: str = "departure"


class FortSummary(FortBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    outbound_count: int = 0
    inbound_count: int = 0
    total_value_out: float = 0.0
    total_value_in: float = 0.0


class VoyageBrief(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    origin_id: Optional[int] = None
    destination_id: Optional[int] = None
    origin_name_raw: Optional[str] = None
    destination_name_raw: Optional[str] = None
    ship_name: str
    captain: Optional[str] = None
    year: Optional[int] = None
    total_gulden: Optional[float] = None
    main_product: Optional[str] = None
    all_products: Optional[str] = None
    destination: Optional[str] = None
    duration_days: Optional[int] = None
    direction: Optional[str] = None
    departure_date: Optional[str] = None
    arrival_date: Optional[str] = None
    cargo_count: Optional[int] = None
    source_url: Optional[str] = None


class FortDetail(FortBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    outbound_voyages: List[VoyageBrief] = []
    inbound_voyages: List[VoyageBrief] = []
    outbound_count: int = 0
    inbound_count: int = 0
    total_value_out: float = 0.0
    total_value_in: float = 0.0
    year_min: Optional[int] = None
    year_max: Optional[int] = None


# ---------- Endpoints ----------

@router.get("/", response_model=List[FortSummary])
async def list_forts(db: AsyncSession = Depends(get_db)):
    """Get all forts with voyage statistics."""
    result = await db.execute(select(Fort))
    forts = result.scalars().all()

    summaries = []
    for fort in forts:
        # Outbound stats
        out_res = await db.execute(
            select(func.count(Voyage.id), func.coalesce(func.sum(Voyage.total_gulden), 0))
            .where(Voyage.origin_id == fort.id)
        )
        out_count, out_total = out_res.one()
        
        # Inbound stats
        in_res = await db.execute(
            select(func.count(Voyage.id), func.coalesce(func.sum(Voyage.total_gulden), 0))
            .where(Voyage.destination_id == fort.id)
        )
        in_count, in_total = in_res.one()

        summaries.append(FortSummary(
            id=fort.id,
            name=fort.name,
            latitude=fort.latitude,
            longitude=fort.longitude,
            color=fort.color,
            description=fort.description,
            port_type=fort.port_type,
            outbound_count=out_count,
            inbound_count=in_count,
            total_value_out=float(out_total or 0),
            total_value_in=float(in_total or 0),
        ))
    return summaries


@router.get("/{fort_id}", response_model=FortDetail)
async def get_fort(fort_id: int, db: AsyncSession = Depends(get_db)):
    """Get fort details with full voyage list."""
    result = await db.execute(select(Fort).where(Fort.id == fort_id))
    fort = result.scalar_one_or_none()
    if not fort:
        raise HTTPException(status_code=404, detail=f"Fort with id={fort_id} not found")

    outbound_res = await db.execute(
        select(Voyage).where(Voyage.origin_id == fort_id).order_by(Voyage.year)
    )
    outbound_voyages = outbound_res.scalars().all()

    inbound_res = await db.execute(
        select(Voyage).where(Voyage.destination_id == fort_id).order_by(Voyage.year)
    )
    inbound_voyages = inbound_res.scalars().all()

    out_stats = await db.execute(
        select(
            func.count(Voyage.id),
            func.coalesce(func.sum(Voyage.total_gulden), 0),
            func.min(Voyage.year),
            func.max(Voyage.year),
        ).where(Voyage.origin_id == fort_id)
    )
    out_count, out_total, out_min, out_max = out_stats.one()

    in_stats = await db.execute(
        select(
            func.count(Voyage.id),
            func.coalesce(func.sum(Voyage.total_gulden), 0),
            func.min(Voyage.year),
            func.max(Voyage.year),
        ).where(Voyage.destination_id == fort_id)
    )
    in_count, in_total, in_min, in_max = in_stats.one()

    # Determine global year range for this fort
    all_years = [y for y in [out_min, out_max, in_min, in_max] if y is not None]

    return FortDetail(
        id=fort.id,
        name=fort.name,
        latitude=fort.latitude,
        longitude=fort.longitude,
        color=fort.color,
        description=fort.description,
        port_type=fort.port_type,
        outbound_voyages=[VoyageBrief.model_validate(v) for v in outbound_voyages],
        inbound_voyages=[VoyageBrief.model_validate(v) for v in inbound_voyages],
        outbound_count=out_count,
        inbound_count=in_count,
        total_value_out=float(out_total or 0),
        total_value_in=float(in_total or 0),
        year_min=min(all_years) if all_years else None,
        year_max=max(all_years) if all_years else None,
    )


@router.get("/{fort_id}/voyages", response_model=List[VoyageBrief])
async def list_fort_voyages(
    fort_id: int,
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
    product: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """Get voyages for a specific fort with optional filters."""
    result = await db.execute(select(Fort).where(Fort.id == fort_id))
    fort = result.scalar_one_or_none()
    if not fort:
        raise HTTPException(status_code=404, detail=f"Fort with id={fort_id} not found")

    query = select(Voyage).where((Voyage.origin_id == fort_id) | (Voyage.destination_id == fort_id))
    if year_from:
        query = query.where(Voyage.year >= year_from)
    if year_to:
        query = query.where(Voyage.year <= year_to)
    if product:
        query = query.where(Voyage.all_products.ilike(f"%{product}%"))

    voy_result = await db.execute(query.order_by(Voyage.year))
    voyages = voy_result.scalars().all()
    return [VoyageBrief.model_validate(v) for v in voyages]


@router.get("/routes/all", tags=["Map"])
async def list_all_routes(db: AsyncSession = Depends(get_db)):
    """A summary of all voyage routes for map visualization."""
    # We aggregate by origin/destination to get route counts
    query = (
        select(
            Voyage.origin_name_raw.label("origin_name"),
            Voyage.destination_name_raw.label("destination_name"),
            func.count(Voyage.id).label("count"),
            func.coalesce(func.sum(Voyage.total_gulden), 0).label("total_value")
        )
        .group_by(Voyage.origin_name_raw, Voyage.destination_name_raw)
        .order_by(func.count(Voyage.id).desc())
    )
    
    result = await db.execute(query)
    routes = result.all()
    
    return [
        {
            "origin_name": r.origin_name,
            "destination_name": r.destination_name,
            "count": r.count,
            "total_value": float(r.total_value)
        }
        for r in routes
    ]
