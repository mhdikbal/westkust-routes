from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func
from pydantic import BaseModel, ConfigDict

from database import get_db
from models import Voyage, Fort

router = APIRouter()


# ---------- Schemas ----------

class VoyageSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    voyage_ref: Optional[int] = None
    origin_id: Optional[int] = None
    destination_id: Optional[int] = None
    origin_name_raw: Optional[str] = None
    destination_name_raw: Optional[str] = None
    ship_name: str
    captain: Optional[str] = None
    tonnage: Optional[str] = None
    year: Optional[int] = None
    departure_date: Optional[str] = None
    arrival_date: Optional[str] = None
    total_gulden: Optional[float] = None
    main_product: Optional[str] = None
    all_products: Optional[str] = None
    cargo_count: Optional[int] = None
    duration_days: Optional[int] = None
    direction: Optional[str] = None
    source_url: Optional[str] = None


class RouteAggregation(BaseModel):
    """Aggregated route data for map visualization."""
    origin_name: Optional[str] = None
    destination_name: Optional[str] = None
    origin_lat: Optional[float] = None
    origin_lon: Optional[float] = None
    dest_lat: Optional[float] = None
    dest_lon: Optional[float] = None
    direction: Optional[str] = None
    count: int
    total_value: float


class VoyageStatsResponse(BaseModel):
    """Overall voyage statistics."""
    total_voyages: int
    total_cargo_value: float
    outbound_count: int
    inbound_count: int
    transit_count: int
    year_min: Optional[int] = None
    year_max: Optional[int] = None
    top_products: List[dict]
    ports: List[dict]


# ---------- Endpoints ----------

@router.get("/", response_model=List[VoyageSchema])
async def list_voyages(
    origin_id: Optional[int] = None,
    destination_id: Optional[int] = None,
    direction: Optional[str] = None,  # "outbound" or "inbound"
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
    product: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = Query(default=200, le=5000),
    db: AsyncSession = Depends(get_db),
):
    """List all voyages with optional filters."""
    query = select(Voyage)
    
    if origin_id is not None:
        query = query.where(Voyage.origin_id == origin_id)
    if destination_id is not None:
        query = query.where(Voyage.destination_id == destination_id)
    if direction:
        query = query.where(Voyage.direction == direction.lower())
        
    if year_from:
        query = query.where(Voyage.year >= year_from)
    if year_to:
        query = query.where(Voyage.year <= year_to)
    if product:
        query = query.where(Voyage.all_products.ilike(f"%{product}%"))
    if search:
        query = query.where(Voyage.ship_name.ilike(f"%{search}%"))

    query = query.order_by(Voyage.year.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/stats", response_model=VoyageStatsResponse)
async def get_voyage_stats(
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
    direction: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """Get aggregated voyage statistics."""
    base_filter = []
    if year_from:
        base_filter.append(Voyage.year >= year_from)
    if year_to:
        base_filter.append(Voyage.year <= year_to)
    if direction:
        base_filter.append(Voyage.direction == direction.lower())

    # Total counts
    q = select(
        func.count(Voyage.id),
        func.coalesce(func.sum(Voyage.total_gulden), 0),
        func.min(Voyage.year),
        func.max(Voyage.year),
    ).where(*base_filter) if base_filter else select(
        func.count(Voyage.id),
        func.coalesce(func.sum(Voyage.total_gulden), 0),
        func.min(Voyage.year),
        func.max(Voyage.year),
    )
    
    result = await db.execute(q)
    total, total_val, y_min, y_max = result.one()

    # Direction counts
    dir_q = select(
        Voyage.direction,
        func.count(Voyage.id),
    ).group_by(Voyage.direction)
    if base_filter:
        for f in base_filter:
            dir_q = dir_q.where(f)
    dir_result = await db.execute(dir_q)
    dir_counts = {row[0]: row[1] for row in dir_result.all()}

    # Top products
    prod_q = select(
        Voyage.main_product,
        func.count(Voyage.id).label("cnt"),
    ).where(Voyage.main_product.isnot(None)).group_by(Voyage.main_product).order_by(desc("cnt")).limit(10)
    if base_filter:
        for f in base_filter:
            prod_q = prod_q.where(f)
    prod_result = await db.execute(prod_q)
    top_products = [{"name": r[0], "count": r[1]} for r in prod_result.all()]

    # Per-port stats
    port_q = select(
        Fort.name,
        Fort.port_type,
        func.count(Voyage.id).label("cnt"),
        func.coalesce(func.sum(Voyage.total_gulden), 0).label("val"),
    ).outerjoin(Voyage, (Voyage.origin_id == Fort.id) | (Voyage.destination_id == Fort.id))
    if base_filter:
        for f in base_filter:
            port_q = port_q.where(f)
    port_q = port_q.group_by(Fort.name, Fort.port_type).order_by(desc("cnt"))
    port_result = await db.execute(port_q)
    ports = [{"name": r[0], "port_type": r[1], "count": r[2], "value": float(r[3])} for r in port_result.all()]

    return VoyageStatsResponse(
        total_voyages=total,
        total_cargo_value=float(total_val),
        outbound_count=dir_counts.get("outbound", 0),
        inbound_count=dir_counts.get("inbound", 0),
        transit_count=dir_counts.get("transit", 0),
        year_min=y_min,
        year_max=y_max,
        top_products=top_products,
        ports=ports,
    )


@router.get("/routes", response_model=List[RouteAggregation])
async def get_voyage_routes(
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
    direction: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """
    Aggregated route data for map visualization.
    Groups voyages by origin→destination pair with counts and total values.
    Includes lat/lon coordinates for each endpoint.
    """
    OriginFort = Fort.__table__.alias("origin_fort")
    DestFort = Fort.__table__.alias("dest_fort")

    query = (
        select(
            OriginFort.c.name.label("origin_name"),
            DestFort.c.name.label("destination_name"),
            OriginFort.c.latitude.label("origin_lat"),
            OriginFort.c.longitude.label("origin_lon"),
            DestFort.c.latitude.label("dest_lat"),
            DestFort.c.longitude.label("dest_lon"),
            Voyage.direction,
            func.count(Voyage.id).label("count"),
            func.coalesce(func.sum(Voyage.total_gulden), 0).label("total_value"),
        )
        .outerjoin(OriginFort, Voyage.origin_id == OriginFort.c.id)
        .outerjoin(DestFort, Voyage.destination_id == DestFort.c.id)
    )

    if year_from:
        query = query.where(Voyage.year >= year_from)
    if year_to:
        query = query.where(Voyage.year <= year_to)
    if direction:
        query = query.where(Voyage.direction == direction.lower())

    # Only include routes where at least one end is a known port
    query = query.where(
        (Voyage.origin_id.isnot(None)) | (Voyage.destination_id.isnot(None))
    )

    query = query.group_by(
        OriginFort.c.name,
        DestFort.c.name,
        OriginFort.c.latitude,
        OriginFort.c.longitude,
        DestFort.c.latitude,
        DestFort.c.longitude,
        Voyage.direction,
    ).order_by(desc("count"))

    result = await db.execute(query)
    routes = result.all()

    return [
        RouteAggregation(
            origin_name=r.origin_name,
            destination_name=r.destination_name,
            origin_lat=r.origin_lat,
            origin_lon=r.origin_lon,
            dest_lat=r.dest_lat,
            dest_lon=r.dest_lon,
            direction=r.direction,
            count=r.count,
            total_value=float(r.total_value),
        )
        for r in routes
    ]


@router.get("/{voyage_id}", response_model=VoyageSchema)
async def get_voyage(voyage_id: int, db: AsyncSession = Depends(get_db)):
    """Get a single voyage by ID."""
    result = await db.execute(select(Voyage).where(Voyage.id == voyage_id))
    voyage = result.scalar_one_or_none()
    if not voyage:
        raise HTTPException(status_code=404, detail=f"Voyage with id={voyage_id} not found")
    return voyage
