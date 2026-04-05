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


class FortSummary(FortBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    voyage_count: int = 0
    total_value: float = 0.0


class VoyageBrief(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    ship_name: str
    captain: Optional[str]
    year: Optional[int]
    total_gulden: Optional[float]
    main_product: Optional[str]
    all_products: Optional[str]
    destination: Optional[str]
    source_url: Optional[str]


class FortDetail(FortBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    voyages: List[VoyageBrief] = []
    voyage_count: int = 0
    total_value: float = 0.0
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
        voy_result = await db.execute(
            select(func.count(Voyage.id), func.coalesce(func.sum(Voyage.total_gulden), 0))
            .where(Voyage.fort_id == fort.id)
        )
        count, total = voy_result.one()
        summaries.append(FortSummary(
            id=fort.id,
            name=fort.name,
            latitude=fort.latitude,
            longitude=fort.longitude,
            color=fort.color,
            description=fort.description,
            voyage_count=count,
            total_value=float(total or 0),
        ))
    return summaries


@router.get("/{fort_id}", response_model=FortDetail)
async def get_fort(fort_id: int, db: AsyncSession = Depends(get_db)):
    """Get fort details with full voyage list."""
    result = await db.execute(select(Fort).where(Fort.id == fort_id))
    fort = result.scalar_one_or_none()
    if not fort:
        raise HTTPException(status_code=404, detail=f"Fort with id={fort_id} not found")

    voy_result = await db.execute(
        select(Voyage).where(Voyage.fort_id == fort_id).order_by(Voyage.year)
    )
    voyages = voy_result.scalars().all()

    stats_result = await db.execute(
        select(
            func.count(Voyage.id),
            func.coalesce(func.sum(Voyage.total_gulden), 0),
            func.min(Voyage.year),
            func.max(Voyage.year),
        ).where(Voyage.fort_id == fort_id)
    )
    count, total, year_min, year_max = stats_result.one()

    return FortDetail(
        id=fort.id,
        name=fort.name,
        latitude=fort.latitude,
        longitude=fort.longitude,
        color=fort.color,
        description=fort.description,
        voyages=[VoyageBrief.model_validate(v) for v in voyages],
        voyage_count=count,
        total_value=float(total or 0),
        year_min=year_min,
        year_max=year_max,
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

    query = select(Voyage).where(Voyage.fort_id == fort_id)
    if year_from:
        query = query.where(Voyage.year >= year_from)
    if year_to:
        query = query.where(Voyage.year <= year_to)
    if product:
        query = query.where(Voyage.all_products.ilike(f"%{product}%"))

    voy_result = await db.execute(query.order_by(Voyage.year))
    voyages = voy_result.scalars().all()
    return [VoyageBrief.model_validate(v) for v in voyages]
