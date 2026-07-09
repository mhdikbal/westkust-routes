"""
Namespace `research` — endpoint thesis-only (BUKAN peta publik /atlas).
SNK-2: Sankey tema-korpus 3-tingkat (dekade -> tema_dominan -> pelabuhan).

Sumber: tabel research_theme_rows (hasil klasifikasi zero-shot GLOBALISE +
Dagh-register, dimuat via seed_research_tema.py). Lihat docs/prd-sankey-tema-korpus.md.
"""
from collections import defaultdict
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import ResearchThemeRow
# reuse skema Sankey yang sudah ada (PRD: "format sama dgn SankeyResponse")
from routers.voyages import SankeyResponse, SankeyNode, SankeyLink

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
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    """Sankey 3-tingkat dekade -> tema -> pelabuhan. Link weight = jumlah kontribusi
    baris (baris multi-pelabuhan menyumbang ke tiap pelabuhannya — FIX #2). Aliran
    konservatif: total dekade->tema == total tema->pelabuhan."""
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
        return SankeyResponse(nodes=[], links=[])

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
    return SankeyResponse(nodes=nodes, links=links)


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
    substring. Filter tahun NULL-inclusive (konsisten SNK-2)."""
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
    return rows[skip: skip + limit]


# ─── SNK-5: triples ringkas utk render Sankey + filter tahun client-side ──────

class SankeyTriplesResponse(BaseModel):
    """Agregasi (dekade, tema, pelabuhan) -> [n, n_lowconf] + meta ringkas, tanpa
    teks penuh — dipakai halaman Django /riset/tema utk membangun Sankey & filter
    tahun sepenuhnya di klien. Teks asli diambil terpisah lewat /rows saat drill."""
    meta: dict
    triples: List[list]


@router.get("/sankey-tema/triples", response_model=SankeyTriplesResponse)
async def get_sankey_tema_triples(db: AsyncSession = Depends(get_db)):
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
    return SankeyTriplesResponse(meta=meta, triples=triples)
