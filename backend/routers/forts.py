import hashlib
import json
import os
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import BaseModel, ConfigDict

from cache import make_key, cache_get, cache_set
from database import get_db
from models import Fort, Voyage, PortArrivalTally, LinimasaEvent, FortModelMetric
from routers.voyages import _year_gte, _year_lte

router = APIRouter()

# ---------- Provenance artifact (Phase B audit, read-only join) ----------
# Separate, nonproduction artifact -- NOT a schema change, NOT
# linimasa_events.csv. Lives under the ./data bind mount (Docker Compose
# ships ./data:/app/data), so it can be updated without a backend rebuild.
# Loaded once at import time; if absent, provenance is simply omitted from
# responses (fail-open, never 500s the endpoint) -- see PROVENANCE_ARTIFACT
# below and _provenance_for_event().
_PROVENANCE_ARTIFACT_PATH = "/app/data/provenance/provenance_artifact.json"


def _load_provenance_artifact():
    try:
        with open(_PROVENANCE_ARTIFACT_PATH, encoding="utf-8") as f:
            return json.load(f).get("events", {})
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}


PROVENANCE_ARTIFACT = _load_provenance_artifact()


def _provenance_join_hash(source_document: str, source_page, book_page, event_date_raw: str, title: str) -> str:
    """Same deterministic join key as Phase B's stable event_id
    (docs/thesis/pilot_annotation/MODEL_3B_EVENT_SOURCE_PROVENANCE_AUDIT.md).
    book_page NULL -> "" to match csv.DictReader's empty-field convention,
    which is what the artifact was built from (backend/scripts/
    verify_provenance_join.py documents and tests this normalization)."""
    sp = str(source_page)
    bp = book_page or ""
    return hashlib.sha1(f"{source_document}|{sp}|{bp}|{event_date_raw}|{title}".encode("utf-8")).hexdigest()[:4]


def _provenance_for_event(source_document, source_page, book_page, event_date_raw, title) -> Optional[dict]:
    """Look up provenance for one LinimasaEvent row. Returns None if the
    artifact is missing/stale/unmatched -- callers must treat that as
    "no provenance data available", never as an error."""
    if not PROVENANCE_ARTIFACT:
        return None
    h = _provenance_join_hash(source_document, source_page, book_page, event_date_raw, title)
    return PROVENANCE_ARTIFACT.get(h)


# ---------- Schemas ----------

class FortBase(BaseModel):
    name: str
    latitude: float
    longitude: float
    color: str
    description: Optional[str] = None
    port_type: str = "departure"
    # Benteng VOC/EIC fisik (garnisun) vs negeri/pusat kekuasaan lokal yang
    # cuma berkorespondensi/traktat dgn VOC -- lihat is_fortified() di bawah.
    is_fortified: bool = True


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


class FortEnrichmentResponse(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float
    port_type: str
    nama_historis: Optional[str] = None
    designasi_voc: Optional[str] = None
    fungsi_historis: Optional[str] = None
    periode_aktif: Optional[str] = None
    amh_url: Optional[str] = None
    amh_images: Optional[list] = None
    outbound_count: int = 0
    inbound_count: int = 0
    total_value_out: float = 0.0
    total_value_in: float = 0.0
    # P1.2 (docs/prd/prd-port-tally-aggregate.md) -- dari port_arrival_tallies, data
    # Dagh-register confidence_flag=unverified, TIDAK dijamin sudah direview manual.
    tally_ship_count: int = 0
    tally_person_count: int = 0


# ---------- Helpers ----------

# EIC forts fisik yang namanya sendiri sudah membuktikan status berbenteng,
# tapi belum di-enrich AMH (designasi_voc kosong) -- lihat
# docs/prd/prd-atlas-power-model-fase2-roster.md. Hapus entri di sini begitu
# enrichment AMH utk kedua fort ini selesai (designasi_voc akan terisi sendiri).
_KNOWN_FORTIFIED_WITHOUT_AMH = {"Fort York", "Fort Marlborough"}


def _is_fortified(fort: Fort) -> bool:
    """True = benteng VOC/EIC fisik (garnisun), False = negeri/pusat kekuasaan
    lokal yang cuma berkorespondensi/traktat dgn VOC (mis. Bayang, Painan,
    Salido, Pauh -- lihat linimasa_events dominion_status utk fort2 ini,
    semuanya traktat/diplomasi/gelar, bukan pembangunan benteng)."""
    return fort.designasi_voc is not None or fort.name in _KNOWN_FORTIFIED_WITHOUT_AMH


# ---------- Endpoints ----------

@router.get("/", response_model=List[FortSummary])
async def list_forts(response: Response, db: AsyncSession = Depends(get_db)):
    """Get all forts with voyage statistics. Cache-aside Redis (ADR-001)."""
    cache_key = make_key("forts", None)
    cached = await cache_get(cache_key)
    if cached is not None:
        response.headers["X-Cache"] = "HIT"
        return cached

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
        
        # Inbound stats — exclude self-referential (origin == destination same fort)
        in_res = await db.execute(
            select(func.count(Voyage.id), func.coalesce(func.sum(Voyage.total_gulden), 0))
            .where(Voyage.destination_id == fort.id)
            .where(Voyage.origin_id != fort.id)
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
            is_fortified=_is_fortified(fort),
            outbound_count=out_count,
            inbound_count=in_count,
            total_value_out=float(out_total or 0),
            total_value_in=float(in_total or 0),
        ))

    payload = [sm.model_dump() for sm in summaries]
    await cache_set(cache_key, payload)
    response.headers["X-Cache"] = "MISS"
    return payload


@router.get("/compare", response_model=dict)
async def compare_ports(
    ids: str = Query(..., description="Comma-separated fort IDs, e.g. '1,3,9'"),
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    """
    Side-by-side comparison of multiple ports.
    Returns stats, trends, and top products for each selected port.
    """
    fort_ids = [int(x.strip()) for x in ids.split(",") if x.strip().isdigit()]
    if len(fort_ids) < 2:
        raise HTTPException(status_code=400, detail="At least 2 port IDs required")
    if len(fort_ids) > 5:
        raise HTTPException(status_code=400, detail="Maximum 5 ports for comparison")

    year_filters = []
    if year_from:
        year_filters.append(_year_gte(year_from))
    if year_to:
        year_filters.append(_year_lte(year_to))

    ports = []
    for fid in fort_ids:
        fort_res = await db.execute(select(Fort).where(Fort.id == fid))
        fort = fort_res.scalar_one_or_none()
        if not fort:
            continue

        # Base query for this port
        base = (Voyage.origin_id == fid) | (Voyage.destination_id == fid)

        # Total stats
        stats_q = select(
            func.count(Voyage.id),
            func.coalesce(func.sum(Voyage.total_gulden), 0),
        ).where(base)
        for yf in year_filters:
            stats_q = stats_q.where(yf)
        stats_res = await db.execute(stats_q)
        total_voyages, total_value = stats_res.one()

        # Outbound/inbound counts — exclude self-referential from inbound
        out_q = select(func.count(Voyage.id)).where(Voyage.origin_id == fid)
        in_q = select(func.count(Voyage.id)).where(Voyage.destination_id == fid).where(Voyage.origin_id != fid)
        for yf in year_filters:
            out_q = out_q.where(yf)
            in_q = in_q.where(yf)
        out_count = (await db.execute(out_q)).scalar() or 0
        in_count = (await db.execute(in_q)).scalar() or 0

        # Top products
        prod_q = (
            select(Voyage.main_product, func.count(Voyage.id).label("cnt"))
            .where(base, Voyage.main_product.isnot(None))
        )
        for yf in year_filters:
            prod_q = prod_q.where(yf)
        prod_q = prod_q.group_by(Voyage.main_product).order_by(func.count(Voyage.id).desc()).limit(8)
        prod_res = await db.execute(prod_q)
        top_products = [{"name": r[0], "count": r[1]} for r in prod_res.all()]

        # Yearly trend
        trend_q = (
            select(
                Voyage.year,
                func.count(Voyage.id).label("count"),
                func.coalesce(func.sum(Voyage.total_gulden), 0).label("value"),
            )
            .where(base, Voyage.year.isnot(None))
        )
        for yf in year_filters:
            trend_q = trend_q.where(yf)
        trend_q = trend_q.group_by(Voyage.year).order_by(Voyage.year)
        trend_res = await db.execute(trend_q)
        yearly_trend = [
            {"year": r.year, "count": r.count, "value": float(r.value)}
            for r in trend_res.all()
        ]

        ports.append({
            "id": fort.id,
            "name": fort.name,
            "color": fort.color,
            "port_type": fort.port_type,
            "total_voyages": total_voyages,
            "outbound": out_count,
            "inbound": in_count,
            "total_value": float(total_value),
            "avg_cargo_value": round(float(total_value) / total_voyages, 2) if total_voyages > 0 else 0,
            "top_products": top_products,
            "yearly_trend": yearly_trend,
        })

    return {"ports": ports}


@router.get("/routes/all", tags=["Map"])
async def list_all_routes(response: Response, db: AsyncSession = Depends(get_db)):
    """A summary of all voyage routes for map visualization. Cache-aside Redis."""
    cache_key = make_key("forts-routes", None)
    cached = await cache_get(cache_key)
    if cached is not None:
        response.headers["X-Cache"] = "HIT"
        return cached

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

    payload = [
        {
            "origin_name": r.origin_name,
            "destination_name": r.destination_name,
            "count": r.count,
            "total_value": float(r.total_value)
        }
        for r in routes
    ]
    await cache_set(cache_key, payload)
    response.headers["X-Cache"] = "MISS"
    return payload


class ProvenanceInfo(BaseModel):
    """Read-only join result from the Phase B provenance audit (141/141
    events). NOT derived from a database column -- see PROVENANCE_ARTIFACT
    above. Absent (None on the parent field) when the artifact doesn't cover
    this event or hasn't been generated -- frontend must treat that as
    "no badge", never as an error or as PROVENANCE_AMBIGUOUS.

    SEMANTIC GUARD: this describes the provenance of ONE historical event
    (as_of_event below) -- the specific dated record currently qualifying
    as a fort's "latest status as of year Y". It is NOT a property of the
    fort or location itself, and must never be read as such. A fort's
    dominion_status changes over time as different events qualify at
    different years; each such event carries its own, independent
    provenance. This is why `provenance` is nested inside `PowerStatusEvent`
    (as_of_event.provenance), not a sibling field on PowerStatusItem --
    the API shape itself should make "this is the event's provenance, not
    the fort's" impossible to misread."""
    status: str
    label: str
    tooltip: str
    researcher_review_required: bool
    multi_source_verified: bool


class PowerStatusEvent(BaseModel):
    id: int
    year: Optional[int] = None
    event_date_raw: Optional[str] = None
    title: str
    text_asli: str
    source_document: str
    provenance: Optional[ProvenanceInfo] = None


class PowerStatusItem(BaseModel):
    fort_id: int
    fort_name: str
    dominion_status: str
    as_of_event: PowerStatusEvent
    # Model 2/5/6 (Markov/System Dynamics/Game Theory) -- opsional, None kalau
    # fort blm py baris fort_model_metrics (mis. blm di-seed ulang pasca Fase 2
    # roster) ATAU n<2 event (model5 skip simulate_fort). Lihat memory
    # project_padang_hinterland_gaps arahan MLOPS+DBA.
    cluster: Optional[str] = None
    p_self_current_status: Optional[float] = None
    dynamics_series: Optional[list] = None
    rmse: Optional[float] = None


@router.get("/power-status", response_model=List[PowerStatusItem], tags=["Map"])
async def get_power_status(
    response: Response,
    year: int = Query(...),
    db: AsyncSession = Depends(get_db),
):
    """Status kekuasaan tiap fort pada tahun `year` (docs/prd/prd-atlas-power-model.md §5):
    untuk tiap fort_id, ambil LinimasaEvent ber-dominion_status TERBARU dgn
    year <= `year`. Fort tanpa event kualifikasi TIDAK muncul di response --
    bukan dikirim dgn status netral/default (PRD §5). Cache-aside Redis, pola
    sama /routes/all."""
    cache_key = make_key("forts-power-status", {"year": year})
    cached = await cache_get(cache_key)
    if cached is not None:
        response.headers["X-Cache"] = "HIT"
        return cached

    query = (
        select(
            LinimasaEvent.fort_id,
            Fort.name.label("fort_name"),
            LinimasaEvent.dominion_status,
            LinimasaEvent.id.label("event_id"),
            LinimasaEvent.year,
            LinimasaEvent.event_date_raw,
            LinimasaEvent.title,
            LinimasaEvent.text_asli,
            LinimasaEvent.source_document,
            # source_page/book_page: not shown in the response body itself --
            # needed only to recompute the Phase B provenance join key
            # (_provenance_join_hash). Selecting them is an additive change
            # to an existing query, not a schema change.
            LinimasaEvent.source_page,
            LinimasaEvent.book_page,
            FortModelMetric.cluster,
            FortModelMetric.p_self_current_status,
            FortModelMetric.dynamics_series,
            FortModelMetric.rmse,
        )
        .join(Fort, Fort.id == LinimasaEvent.fort_id)
        # LEFT JOIN -- fort_model_metrics OPSIONAL, kolom model harus None
        # (bukan 500/fort hilang) kalau blm pernah di-seed_fort_model_metrics.py
        .outerjoin(FortModelMetric, FortModelMetric.fort_id == LinimasaEvent.fort_id)
        .where(LinimasaEvent.fort_id.isnot(None))
        .where(LinimasaEvent.dominion_status.isnot(None))
        # JANGAN pakai _linimasa_year_lte (NULL-safe) di sini -- Postgres DESC
        # default NULLS FIRST bikin event ber-year=NULL menang "terbaru" di
        # DISTINCT ON apapun tahun yg diminta. Filter NULL eksplisit dulu.
        .where(LinimasaEvent.year.isnot(None))
        .where(LinimasaEvent.year <= year)
        .distinct(LinimasaEvent.fort_id)
        .order_by(LinimasaEvent.fort_id, LinimasaEvent.year.desc(), LinimasaEvent.id.desc())
    )
    rows = (await db.execute(query)).all()

    payload = []
    for r in rows:
        prov = _provenance_for_event(
            r.source_document, r.source_page, r.book_page, r.event_date_raw, r.title
        )
        payload.append(
            PowerStatusItem(
                fort_id=r.fort_id,
                fort_name=r.fort_name,
                dominion_status=r.dominion_status,
                as_of_event=PowerStatusEvent(
                    id=r.event_id,
                    year=r.year,
                    event_date_raw=r.event_date_raw,
                    title=r.title,
                    text_asli=r.text_asli,
                    source_document=r.source_document,
                    provenance=ProvenanceInfo(
                        status=prov["provenance_status"],
                        label=prov["provenance_label"],
                        tooltip=prov["provenance_tooltip"],
                        researcher_review_required=prov["researcher_review_required"],
                        multi_source_verified=prov["multi_source_verified"],
                    ) if prov else None,
                ),
                cluster=r.cluster,
                p_self_current_status=r.p_self_current_status,
                dynamics_series=r.dynamics_series,
                rmse=r.rmse,
            ).model_dump()
        )
    await cache_set(cache_key, payload)
    response.headers["X-Cache"] = "MISS"
    return payload


@router.get("/{fort_id}/enrichment", response_model=FortEnrichmentResponse, tags=["Enrichment"])
async def get_fort_enrichment(fort_id: int, db: AsyncSession = Depends(get_db)):
    """Get fort enrichment data including historical metadata and voyage statistics."""
    result = await db.execute(select(Fort).where(Fort.id == fort_id))
    fort = result.scalar_one_or_none()
    if not fort:
        raise HTTPException(status_code=404, detail=f"Fort with id={fort_id} not found")

    out_res = await db.execute(
        select(func.count(Voyage.id), func.coalesce(func.sum(Voyage.total_gulden), 0))
        .where(Voyage.origin_id == fort_id)
    )
    out_count, out_total = out_res.one()

    in_res = await db.execute(
        select(func.count(Voyage.id), func.coalesce(func.sum(Voyage.total_gulden), 0))
        .where(Voyage.destination_id == fort_id)
        .where(Voyage.origin_id != fort_id)
    )
    in_count, in_total = in_res.one()

    tally_res = await db.execute(
        select(
            func.coalesce(func.sum(PortArrivalTally.ship_count), 0),
            func.coalesce(func.sum(PortArrivalTally.person_count), 0),
        )
        .where(PortArrivalTally.origin_fort_id == fort_id)
        .where(PortArrivalTally.confidence_flag != "rejected")
    )
    tally_ship_count, tally_person_count = tally_res.one()

    periode_str: Optional[str] = None
    if fort.periode_aktif is not None:
        pa = fort.periode_aktif
        lower = pa.lower
        upper = pa.upper
        if lower is not None and upper is not None:
            periode_str = f"{lower}-{upper}"
        elif lower is not None:
            periode_str = str(lower)
        elif upper is not None:
            periode_str = str(upper)

    return FortEnrichmentResponse(
        id=fort.id,
        name=fort.name,
        latitude=fort.latitude,
        longitude=fort.longitude,
        port_type=fort.port_type,
        nama_historis=fort.nama_historis,
        designasi_voc=fort.designasi_voc,
        fungsi_historis=fort.fungsi_historis,
        periode_aktif=periode_str,
        amh_url=fort.amh_url,
        amh_images=fort.amh_images,
        outbound_count=out_count,
        inbound_count=in_count,
        total_value_out=float(out_total or 0),
        total_value_in=float(in_total or 0),
        tally_ship_count=int(tally_ship_count or 0),
        tally_person_count=int(tally_person_count or 0),
    )


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
        select(Voyage)
        .where(Voyage.destination_id == fort_id)
        .where(Voyage.origin_id != fort_id)
        .order_by(Voyage.year)
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
        )
        .where(Voyage.destination_id == fort_id)
        .where(Voyage.origin_id != fort_id)
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
        query = query.where(_year_gte(year_from))
    if year_to:
        query = query.where(_year_lte(year_to))
    if product:
        query = query.where(Voyage.all_products.ilike(f"%{product}%"))

    voy_result = await db.execute(query.order_by(Voyage.year))
    voyages = voy_result.scalars().all()
    return [VoyageBrief.model_validate(v) for v in voyages]


