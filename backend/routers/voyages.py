from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func
from pydantic import BaseModel, ConfigDict

from database import get_db
from models import Voyage, Fort, CargoItem

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


class CargoItemSchema(BaseModel):
    """Individual cargo item on a voyage."""
    model_config = ConfigDict(from_attributes=True)
    id: int
    voyage_id: int
    produk: str
    spesifikasi: Optional[str] = None
    qty_asli: Optional[str] = None
    unit: Optional[str] = None
    nilai_numerik: Optional[float] = None
    gram: Optional[float] = None
    gulden_nl: Optional[float] = None
    gulden_india: Optional[float] = None
    catatan: Optional[str] = None


class NetworkNode(BaseModel):
    id: str
    lat: float
    lon: float
    port_type: str
    color: str
    total_voyages: int
    total_value: float


class NetworkEdge(BaseModel):
    source: str
    target: str
    weight: int
    total_value: float
    direction: Optional[str] = None


class NetworkResponse(BaseModel):
    nodes: List[NetworkNode]
    edges: List[NetworkEdge]


class HeatmapCell(BaseModel):
    year: int
    port: str
    count: int
    value: float


class HeatmapResponse(BaseModel):
    years: List[int]
    ports: List[str]
    data: List[HeatmapCell]


class SankeyNode(BaseModel):
    name: str


class SankeyLink(BaseModel):
    source: int
    target: int
    value: float


class SankeyResponse(BaseModel):
    nodes: List[SankeyNode]
    links: List[SankeyLink]


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


@router.get("/{voyage_id}/cargo", response_model=List[CargoItemSchema])
async def get_voyage_cargo(voyage_id: int, db: AsyncSession = Depends(get_db)):
    """Get all cargo items for a specific voyage."""
    # Verify voyage exists
    voyage_check = await db.execute(select(Voyage.id).where(Voyage.id == voyage_id))
    if not voyage_check.scalar_one_or_none():
        raise HTTPException(status_code=404, detail=f"Voyage with id={voyage_id} not found")
    
    result = await db.execute(
        select(CargoItem)
        .where(CargoItem.voyage_id == voyage_id)
        .order_by(CargoItem.gulden_india.desc().nullslast())
    )
    return result.scalars().all()


@router.get("/analytics/network", response_model=NetworkResponse)
async def get_network_graph(
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    """Get network graph data: nodes (ports) and edges (routes) with weights."""
    # Build base filters
    filters = []
    if year_from:
        filters.append(Voyage.year >= year_from)
    if year_to:
        filters.append(Voyage.year <= year_to)

    # Nodes: all forts with voyage counts
    forts_result = await db.execute(select(Fort))
    forts = forts_result.scalars().all()
    
    nodes = []
    for fort in forts:
        # Count voyages where this fort is origin or destination
        count_q = select(func.count(Voyage.id)).where(
            (Voyage.origin_id == fort.id) | (Voyage.destination_id == fort.id)
        )
        value_q = select(func.coalesce(func.sum(Voyage.total_gulden), 0)).where(
            (Voyage.origin_id == fort.id) | (Voyage.destination_id == fort.id)
        )
        for f in filters:
            count_q = count_q.where(f)
            value_q = value_q.where(f)
        
        count_res = await db.execute(count_q)
        value_res = await db.execute(value_q)
        total_voyages = count_res.scalar() or 0
        total_value = float(value_res.scalar() or 0)
        
        if total_voyages > 0:
            nodes.append(NetworkNode(
                id=fort.name,
                lat=fort.latitude,
                lon=fort.longitude,
                port_type=fort.port_type,
                color=fort.color,
                total_voyages=total_voyages,
                total_value=total_value,
            ))

    # Edges: aggregated routes
    edge_q = (
        select(
            Fort.name.label("origin_name"),
            func.min(Fort.name).label("_dummy"),  # placeholder
            Voyage.direction,
            func.count(Voyage.id).label("weight"),
            func.coalesce(func.sum(Voyage.total_gulden), 0).label("total_value"),
        )
        .join(Fort, Voyage.origin_id == Fort.id)
        .where(Voyage.origin_id.isnot(None), Voyage.destination_id.isnot(None))
    )
    for f in filters:
        edge_q = edge_q.where(f)
    
    # Need a subquery approach for both fort names
    OriginFort = Fort.__table__.alias("of")
    DestFort = Fort.__table__.alias("df")
    edge_q = (
        select(
            OriginFort.c.name.label("source"),
            DestFort.c.name.label("target"),
            Voyage.direction,
            func.count(Voyage.id).label("weight"),
            func.coalesce(func.sum(Voyage.total_gulden), 0).label("total_value"),
        )
        .join(OriginFort, Voyage.origin_id == OriginFort.c.id)
        .join(DestFort, Voyage.destination_id == DestFort.c.id)
    )
    for f in filters:
        edge_q = edge_q.where(f)
    edge_q = edge_q.group_by(
        OriginFort.c.name, DestFort.c.name, Voyage.direction
    ).order_by(desc("weight"))

    edge_result = await db.execute(edge_q)
    edges = [
        NetworkEdge(
            source=r.source,
            target=r.target,
            weight=r.weight,
            total_value=float(r.total_value),
            direction=r.direction,
        )
        for r in edge_result.all()
    ]

    return NetworkResponse(nodes=nodes, edges=edges)


@router.get("/analytics/heatmap", response_model=HeatmapResponse)
async def get_heatmap(
    metric: str = Query(default="count", regex="^(count|value)$"),
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    """
    Temporal heatmap: year × port matrix.
    Returns count or value for each year-port combination.
    """
    # Get all forts
    forts_result = await db.execute(select(Fort).order_by(Fort.id))
    forts = forts_result.scalars().all()
    port_names = [f.name for f in forts]
    fort_id_map = {f.id: f.name for f in forts}

    # Build query: group by year and port
    # Union of origin and destination to capture both directions
    filters = []
    if year_from:
        filters.append(Voyage.year >= year_from)
    if year_to:
        filters.append(Voyage.year <= year_to)

    # Query for origin port activity
    origin_q = (
        select(
            Voyage.year,
            Voyage.origin_id.label("fort_id"),
            func.count(Voyage.id).label("cnt"),
            func.coalesce(func.sum(Voyage.total_gulden), 0).label("val"),
        )
        .where(Voyage.origin_id.isnot(None), Voyage.year.isnot(None))
    )
    for f in filters:
        origin_q = origin_q.where(f)
    origin_q = origin_q.group_by(Voyage.year, Voyage.origin_id)
    
    origin_result = await db.execute(origin_q)
    
    # Destination port activity
    dest_q = (
        select(
            Voyage.year,
            Voyage.destination_id.label("fort_id"),
            func.count(Voyage.id).label("cnt"),
            func.coalesce(func.sum(Voyage.total_gulden), 0).label("val"),
        )
        .where(Voyage.destination_id.isnot(None), Voyage.year.isnot(None))
    )
    for f in filters:
        dest_q = dest_q.where(f)
    dest_q = dest_q.group_by(Voyage.year, Voyage.destination_id)
    
    dest_result = await db.execute(dest_q)

    # Merge results
    matrix = {}  # (year, port_name) -> {count, value}
    years_set = set()
    
    for row in origin_result.all():
        port_name = fort_id_map.get(row.fort_id)
        if not port_name:
            continue
        key = (row.year, port_name)
        years_set.add(row.year)
        if key not in matrix:
            matrix[key] = {"count": 0, "value": 0.0}
        matrix[key]["count"] += row.cnt
        matrix[key]["value"] += float(row.val)
    
    for row in dest_result.all():
        port_name = fort_id_map.get(row.fort_id)
        if not port_name:
            continue
        key = (row.year, port_name)
        years_set.add(row.year)
        if key not in matrix:
            matrix[key] = {"count": 0, "value": 0.0}
        matrix[key]["count"] += row.cnt
        matrix[key]["value"] += float(row.val)

    years = sorted(years_set)
    data = [
        HeatmapCell(
            year=year,
            port=port,
            count=matrix.get((year, port), {}).get("count", 0),
            value=matrix.get((year, port), {}).get("value", 0.0),
        )
        for year in years
        for port in port_names
    ]

    return HeatmapResponse(years=years, ports=port_names, data=data)


@router.get("/analytics/sankey", response_model=SankeyResponse)
async def get_sankey_data(
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    """
    Generate nodes and links for Sankey commodity flow.
    Origin Port -> Product Category -> Destination Port
    """
    filters = [
        Voyage.main_product.isnot(None), 
        Voyage.origin_name_raw.isnot(None),
        Voyage.destination_name_raw.isnot(None)
    ]
    if year_from:
        filters.append(Voyage.year >= year_from)
    if year_to:
        filters.append(Voyage.year <= year_to)
        
    query = (
        select(
            Voyage.origin_name_raw,
            Voyage.main_product,
            Voyage.destination_name_raw,
            func.coalesce(func.sum(Voyage.total_gulden), 0).label("val")
        )
        .where(*filters)
        .group_by(Voyage.origin_name_raw, Voyage.main_product, Voyage.destination_name_raw)
    )
    result = await db.execute(query)
    rows = result.all()
    
    from collections import defaultdict

    # Calculate top 12 products by value
    prod_totals = defaultdict(float)
    for row in rows:
        prod_totals[str(row.main_product).strip().capitalize()] += float(row.val)
    top_prods = dict(sorted(prod_totals.items(), key=lambda item: item[1], reverse=True)[:12])
    
    node_names = []
    
    def get_or_add_node(name):
        if name not in node_names:
            node_names.append(name)
        return node_names.index(name)
        
    link_map = defaultdict(float)
    
    for row in rows:
        orig = f"{row.origin_name_raw} (Asal)"
        prod_raw = str(row.main_product).strip().capitalize()
        prod = prod_raw if prod_raw in top_prods else "Lainnya"
        dest = f"{row.destination_name_raw} (Tujuan)"
        val = float(row.val)
        if val <= 0:
            continue
        
        # Build flow maps
        link_map[(orig, prod)] += val
        link_map[(prod, dest)] += val
        
    links = []
    for (src, tgt), val in link_map.items():
        s_idx = get_or_add_node(src)
        t_idx = get_or_add_node(tgt)
        links.append({"source": s_idx, "target": t_idx, "value": val})
        
    nodes = [{"name": n} for n in node_names]
    
    return SankeyResponse(nodes=nodes, links=links)
