"""
Namespace `research` — endpoint thesis-only (BUKAN peta publik /atlas).
SNK-2: Sankey tema-korpus 3-tingkat (dekade -> tema_dominan -> pelabuhan).

Sumber: tabel research_theme_rows (hasil klasifikasi zero-shot GLOBALISE +
Dagh-register, dimuat via seed_research_tema.py). Lihat docs/prd-sankey-tema-korpus.md.
"""
from collections import defaultdict
from itertools import combinations
from typing import List, Optional

from fastapi import APIRouter, Depends, Query, Response
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import ResearchThemeRow, AtjehTradeRecord
# reuse skema Sankey yang sudah ada (PRD: "format sama dgn SankeyResponse")
from routers.voyages import SankeyResponse, SankeyNode, SankeyLink
# cache-aside Redis (ADR-001) — degradasi anggun bila Redis mati (cache_get -> None)
from cache import make_key, cache_get, cache_set

router = APIRouter()

NO_YEAR_BUCKET = "Tak bertahun"
UNKNOWN_PORT = "Tidak diketahui"


def _year_gte(value: int):
    """tahun >= value TAPI tahun IS NULL tetap ikut (tidak disenyapkan) — konsisten
    dgn kebijakan _year_gte di voyages.py & [[feedback_sisir_semua_titik_pemakaian]]."""
    return or_(ResearchThemeRow.tahun.is_(None), ResearchThemeRow.tahun >= value)


def _year_lte(value: int):
    return or_(ResearchThemeRow.tahun.is_(None), ResearchThemeRow.tahun <= value)


def _split_ports(raw: Optional[str]):
    """FIX #2: 'Barus; Padang' -> ['Barus','Padang']; kosong -> ['Tidak diketahui']."""
    parts = [p.strip() for p in (raw or "").split(";") if p.strip()]
    return parts or [UNKNOWN_PORT]


@router.get("/sankey-tema", response_model=SankeyResponse)
async def get_sankey_tema(
    response: Response,
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    """Sankey 3-tingkat dekade -> tema -> pelabuhan. Link weight = jumlah kontribusi
    baris (baris multi-pelabuhan menyumbang ke tiap pelabuhannya — FIX #2). Aliran
    konservatif: total dekade->tema == total tema->pelabuhan. Cache-aside Redis."""
    cache_key = make_key("research_sankey", {"year_from": year_from, "year_to": year_to})
    cached = await cache_get(cache_key)
    if cached is not None:
        response.headers["X-Cache"] = "HIT"
        return cached

    filters = []
    if year_from is not None:
        filters.append(_year_gte(year_from))
    if year_to is not None:
        filters.append(_year_lte(year_to))

    query = select(
        ResearchThemeRow.dekade,
        ResearchThemeRow.tema_dominan,
        ResearchThemeRow.pelabuhan_disebut,
    )
    if filters:
        query = query.where(*filters)

    rows = (await db.execute(query)).all()

    # agregasi triple (dekade, tema, pelabuhan) -> jumlah kontribusi
    triple = defaultdict(int)
    for row in rows:
        dek = str(row.dekade) if row.dekade is not None else NO_YEAR_BUCKET
        tema = row.tema_dominan
        for port in _split_ports(row.pelabuhan_disebut):
            triple[(dek, tema, port)] += 1

    if not triple:
        payload = {"nodes": [], "links": []}
        await cache_set(cache_key, payload)
        response.headers["X-Cache"] = "MISS"
        return payload

    # dua tingkat link, diturunkan dari triple yg sama -> konservasi terjaga
    d2t = defaultdict(int)  # (dekade, tema)
    t2p = defaultdict(int)  # (tema, pelabuhan)
    dekades, temas, ports = set(), set(), set()
    for (dek, tema, port), c in triple.items():
        d2t[(dek, tema)] += c
        t2p[(tema, port)] += c
        dekades.add(dek)
        temas.add(tema)
        ports.add(port)

    # urutan node deterministik: dekade (numerik, 'Tak bertahun' terakhir) -> tema -> pelabuhan
    def dek_key(d):
        return (1, 0) if d == NO_YEAR_BUCKET else (0, int(d))

    ordered = (
        sorted(dekades, key=dek_key)
        + sorted(temas)
        + sorted(ports)
    )
    node_index = {name: i for i, name in enumerate(ordered)}

    links = []
    for (dek, tema), c in d2t.items():
        links.append(SankeyLink(source=node_index[dek], target=node_index[tema], value=c))
    for (tema, port), c in t2p.items():
        links.append(SankeyLink(source=node_index[tema], target=node_index[port], value=c))

    nodes = [SankeyNode(name=n) for n in ordered]
    payload = SankeyResponse(nodes=nodes, links=links).model_dump()
    await cache_set(cache_key, payload)
    response.headers["X-Cache"] = "MISS"
    return payload


# ─── SNK-3: drill-down audit ke baris teks asli ──────────────────────────────

class ResearchRowOut(BaseModel):
    """Satu baris klasifikasi utk audit drill-down — transparansi 'kenapa baris
    ini dapat skor segini' (PRD Goal #4). `text` = yang diklasifikasi model;
    `text_asli` = cuplikan Belanda (DR) / pointer inventaris (globalise)."""
    model_config = ConfigDict(from_attributes=True)

    corpus_id: int
    corpus_asal: str
    source: Optional[str] = None
    volume: Optional[str] = None
    inventaris_ref: Optional[str] = None
    tanggal_perkiraan: Optional[str] = None
    tahun: Optional[int] = None
    dekade: Optional[int] = None
    pelabuhan_disebut: str
    tema_dominan: str
    skor_dominan: Optional[float] = None
    low_confidence: bool
    skor_pdr_drainase: Optional[float] = None
    skor_etr_retensi: Optional[float] = None
    skor_hak_adat: Optional[float] = None
    skor_pelayaran: Optional[float] = None
    skor_sengketa: Optional[float] = None
    skor_syahbandar: Optional[float] = None
    skor_tidak_relevan: Optional[float] = None
    text: str
    text_asli: Optional[str] = None


@router.get("/sankey-tema/rows", response_model=List[ResearchRowOut])
async def get_sankey_tema_rows(
    response: Response,
    tema: Optional[str] = None,
    pelabuhan: Optional[str] = None,
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(200, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
):
    """Baris penyusun satu alur Sankey (klik link -> daftar teks asli). Filter
    pelabuhan mencocokkan KEANGGOTAAN token pada baris multi-port (FIX #2), bukan
    substring. Filter tahun NULL-inclusive (konsisten SNK-2). Cache-aside Redis."""
    cache_key = make_key("research_rows", {
        "tema": tema, "pelabuhan": pelabuhan, "year_from": year_from,
        "year_to": year_to, "skip": skip, "limit": limit,
    })
    cached = await cache_get(cache_key)
    if cached is not None:
        response.headers["X-Cache"] = "HIT"
        return cached

    filters = []
    if tema is not None:
        filters.append(ResearchThemeRow.tema_dominan == tema)
    if year_from is not None:
        filters.append(_year_gte(year_from))
    if year_to is not None:
        filters.append(_year_lte(year_to))

    query = select(ResearchThemeRow)
    if filters:
        query = query.where(*filters)
    query = query.order_by(ResearchThemeRow.tahun.is_(None), ResearchThemeRow.tahun, ResearchThemeRow.corpus_id)

    rows = (await db.execute(query)).scalars().all()

    # filter pelabuhan by keanggotaan token (bukan LIKE substring) di Python
    if pelabuhan is not None:
        rows = [r for r in rows if pelabuhan in _split_ports(r.pelabuhan_disebut)]

    # paginasi setelah filter port agar hitungan konsisten
    page = rows[skip: skip + limit]
    payload = [ResearchRowOut.model_validate(r).model_dump() for r in page]
    await cache_set(cache_key, payload)
    response.headers["X-Cache"] = "MISS"
    return payload


# ─── SNK-5: triples ringkas utk render Sankey + filter tahun client-side ──────

class SankeyTriplesResponse(BaseModel):
    """Agregasi (dekade, tema, pelabuhan) -> [n, n_lowconf] + meta ringkas, tanpa
    teks penuh — dipakai halaman Django /riset/tema utk membangun Sankey & filter
    tahun sepenuhnya di klien. Teks asli diambil terpisah lewat /rows saat drill."""
    meta: dict
    triples: List[list]


@router.get("/sankey-tema/triples", response_model=SankeyTriplesResponse)
async def get_sankey_tema_triples(response: Response, db: AsyncSession = Depends(get_db)):
    cache_key = make_key("research_triples", None)
    cached = await cache_get(cache_key)
    if cached is not None:
        response.headers["X-Cache"] = "HIT"
        return cached

    rows = (await db.execute(select(
        ResearchThemeRow.dekade,
        ResearchThemeRow.tema_dominan,
        ResearchThemeRow.pelabuhan_disebut,
        ResearchThemeRow.low_confidence,
        ResearchThemeRow.corpus_asal,
    ))).all()

    trip = defaultdict(lambda: [0, 0])  # (dekade, tema, port) -> [n, n_lowconf]
    temas, decs, ports = set(), set(), set()
    total = n_dagh = n_glob = n_low = 0
    for r in rows:
        total += 1
        if r.corpus_asal == "daghregister":
            n_dagh += 1
        elif r.corpus_asal == "globalise":
            n_glob += 1
        if r.low_confidence:
            n_low += 1
        if r.dekade is not None:
            decs.add(r.dekade)
        temas.add(r.tema_dominan)
        for port in _split_ports(r.pelabuhan_disebut):  # FIX #2: explode multi-port
            ports.add(port)
            trip[(r.dekade, r.tema_dominan, port)][0] += 1
            if r.low_confidence:
                trip[(r.dekade, r.tema_dominan, port)][1] += 1

    triples = [[k[0], k[1], k[2], v[0], v[1]] for k, v in trip.items()]
    meta = {
        "total": total, "n_dagh": n_dagh, "n_glob": n_glob, "n_lowconf": n_low,
        "decades": sorted(decs), "temas": sorted(temas),
        "n_ports": len(ports),
        "contrib": sum(v[0] for v in trip.values()),
    }
    payload = SankeyTriplesResponse(meta=meta, triples=triples).model_dump()
    await cache_set(cache_key, payload)
    response.headers["X-Cache"] = "MISS"
    return payload


# ─── Network Graph Fase 1 (MVP): graf co-occurrence pelabuhan ────────────────
# docs/prd-network-graph-aktor-tema.md §4 Fase 1. 0 GPU/ML: agregasi SQL murni
# dari kolom pelabuhan_disebut (SUDAH ada) + warna edge dari tema_dominan. Layer
# aktor eksternal (VOC/Aceh/China/EIC) via keyword-tag = increment TERPISAH di
# belakang gerbang spot-check 25 baris ([[feedback_verify_entity_extraction_before_trusting]]).

class NetworkNode(BaseModel):
    id: str
    label: str           # display name; utk pelabuhan = id (beda saat Fase 2 aktor)
    weight: int          # jumlah baris yang menyebut pelabuhan ini


class NetworkEdge(BaseModel):
    source: str          # leksikografis < target (edge tak-berarah dinormalisasi)
    target: str
    weight: int          # jumlah baris co-occurrence pasangan ini
    tema: str            # tema_dominan modal antar baris pembentuk edge
    tema_breakdown: dict  # {tema: n} — komposisi bidang relasi (drill/hover)


class NetworkResponse(BaseModel):
    nodes: List[NetworkNode]
    edges: List[NetworkEdge]
    meta: dict


@router.get("/network-pelabuhan", response_model=NetworkResponse)
async def get_network_pelabuhan(
    response: Response,
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
    tema: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """Graf pelabuhan-pelabuhan (Fase 1 MVP). Node=pelabuhan (bobot=jumlah baris
    yang menyebutnya), edge=dua pelabuhan disebut di baris yang sama (bobot=jumlah
    baris co-occurrence), tema edge=tema_dominan modal antar baris pembentuk.
    'Tidak diketahui' di-exclude (bukan entitas). Filter tahun NULL-inclusive
    (konsisten SNK-2). Filter tema=exact-match: hanya baris tema itu membentuk graf
    (categorical, bukan NULL-inclusive) — dilakukan in-Python agar unit-testable via
    mock, biaya diabaikan pada ~1k baris. Cache-aside Redis (degradasi anggun)."""
    cache_key = make_key("research_network_pelabuhan",
                         {"year_from": year_from, "year_to": year_to, "tema": tema})
    cached = await cache_get(cache_key)
    if cached is not None:
        response.headers["X-Cache"] = "HIT"
        return cached

    filters = []
    if year_from is not None:
        filters.append(_year_gte(year_from))
    if year_to is not None:
        filters.append(_year_lte(year_to))

    query = select(
        ResearchThemeRow.pelabuhan_disebut,
        ResearchThemeRow.tema_dominan,
    )
    if filters:
        query = query.where(*filters)
    rows = (await db.execute(query)).all()

    node_weight = defaultdict(int)                       # pelabuhan -> jumlah sebut
    edge_tema = defaultdict(lambda: defaultdict(int))    # (a,b) -> {tema: n}
    n_rows = 0                                            # baris yang lolos filter tema
    n_multiport = 0
    for row in rows:
        if tema is not None and row.tema_dominan != tema:
            continue
        n_rows += 1
        # dedupe + buang UNKNOWN sebelum pairing; sort utk normalisasi arah edge
        ports = sorted({p for p in _split_ports(row.pelabuhan_disebut) if p != UNKNOWN_PORT})
        for p in ports:
            node_weight[p] += 1
        if len(ports) >= 2:
            n_multiport += 1
            for a, b in combinations(ports, 2):
                edge_tema[(a, b)][row.tema_dominan] += 1

    nodes = [NetworkNode(id=p, label=p, weight=w) for p, w in sorted(node_weight.items())]

    edges = []
    for (a, b) in sorted(edge_tema.keys()):
        breakdown = dict(edge_tema[(a, b)])
        # tema modal: bobot tertinggi; tie-break alfabetis (deterministik/cache-friendly)
        modal = max(sorted(breakdown), key=lambda t: breakdown[t])
        edges.append(NetworkEdge(
            source=a, target=b, weight=sum(breakdown.values()),
            tema=modal, tema_breakdown=breakdown,
        ))

    meta = {
        "n_rows": n_rows,
        "n_nodes": len(nodes),
        "n_edges": len(edges),
        "n_multiport": n_multiport,
    }
    payload = NetworkResponse(nodes=nodes, edges=edges, meta=meta).model_dump()
    await cache_set(cache_key, payload)
    response.headers["X-Cache"] = "MISS"
    return payload


# ─── Dagang Atjeh 1643-1644 ──────────────────────────────────────────────────
# Sumber: tabel atjeh_trade_records (hasil ekstraksi manual Dagh-register Batavia
# 1643-1644, dimuat via seed_atjeh_trade.py). commodity_raw/unit_raw/actor_raw
# SENGAJA ejaan asli VOC-Belanda, bukan terjemahan -- lihat CommodityGlossary
# utk padanan. Semua baris confidence_flag='unverified' (blm dicocokkan scan asli).

class AtjehTradeItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    source_page: int
    book_page: Optional[str] = None
    entry_date_raw: Optional[str] = None
    direction: str
    commodity_raw: Optional[str] = None
    quantity_raw: Optional[str] = None
    unit_raw: Optional[str] = None
    price_value: Optional[float] = None
    price_unit_raw: Optional[str] = None
    actor_raw: Optional[str] = None
    text_asli: str
    confidence_flag: str
    notes: Optional[str] = None


class AtjehTradeResponse(BaseModel):
    items: List[AtjehTradeItem]
    meta: dict


@router.get("/atjeh-trade", response_model=AtjehTradeResponse)
async def get_atjeh_trade(
    response: Response,
    direction: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """Daftar baris atjeh_trade_records, urut halaman sumber. Filter direction
    opsional ('naar_atjeh'|'van_atjeh'|'in_atjeh'). Cache-aside Redis."""
    cache_key = make_key("research_atjeh_trade", {"direction": direction})
    cached = await cache_get(cache_key)
    if cached is not None:
        response.headers["X-Cache"] = "HIT"
        return cached

    query = select(AtjehTradeRecord).order_by(
        AtjehTradeRecord.source_page, AtjehTradeRecord.id
    )
    if direction:
        query = query.where(AtjehTradeRecord.direction == direction.lower())
    rows = (await db.execute(query)).scalars().all()

    items = [AtjehTradeItem.model_validate(r) for r in rows]
    by_direction = defaultdict(int)
    for r in rows:
        by_direction[r.direction] += 1

    meta = {"n_items": len(items), "by_direction": dict(by_direction)}
    payload = AtjehTradeResponse(items=items, meta=meta).model_dump()
    await cache_set(cache_key, payload)
    response.headers["X-Cache"] = "MISS"
    return payload
