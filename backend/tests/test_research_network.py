"""
Network Graph Fase 1 (MVP) — Unit tests untuk GET /api/research/network-pelabuhan.
TDD: ditulis SEBELUM implementasi (docs/prd/prd-network-graph-aktor-tema.md §4 Fase 1).

Graf pelabuhan-pelabuhan: node = pelabuhan, edge = dua pelabuhan disebut di baris
yang sama (co-occurrence), bobot edge = jumlah baris, warna/tema edge = tema_dominan
modal antar baris pembentuk edge. "Tidak diketahui" di-exclude (bukan entitas).
Reuse pola mock DB session dari test_research_sankey.py (result.all()).
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from httpx import AsyncClient, ASGITransport
from types import SimpleNamespace

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from database import get_db


def make_row(pelabuhan, tema, dekade=1700, tahun=None):
    if tahun is None and dekade is not None:
        tahun = dekade
    return SimpleNamespace(
        pelabuhan_disebut=pelabuhan, tema_dominan=tema, dekade=dekade, tahun=tahun
    )


def db_returning(rows):
    async def mock_get_db():
        session = AsyncMock()
        result = MagicMock()
        result.all.return_value = rows
        session.execute.return_value = result
        yield session
    return mock_get_db


async def _get(url):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        return await client.get(url)


def _edge(data, a, b):
    """Cari edge tak-berarah {a,b} (source<target sudah dinormalisasi endpoint)."""
    lo, hi = sorted([a, b])
    for e in data["edges"]:
        if e["source"] == lo and e["target"] == hi:
            return e
    return None


def _node(data, nid):
    for n in data["nodes"]:
        if n["id"] == nid:
            return n
    return None


# ─── Happy path / struktur ───────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_basic_structure_and_cooccurrence():
    """Baris multi-port 'Barus; Padang' -> 1 edge Barus-Padang; struktur {nodes,edges,meta}."""
    app.dependency_overrides[get_db] = db_returning([
        make_row("Barus; Padang", "syahbandar"),
    ])
    try:
        r = await _get("/api/research/network-pelabuhan")
        assert r.status_code == 200
        data = r.json()
        assert set(data.keys()) >= {"nodes", "edges", "meta"}
        assert _node(data, "Barus") is not None
        assert _node(data, "Padang") is not None
        e = _edge(data, "Barus", "Padang")
        assert e is not None
        assert e["weight"] == 1
        assert e["tema"] == "syahbandar"
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_source_lt_target_normalized():
    """Edge tak-berarah: source selalu < target secara leksikografis (deterministik)."""
    app.dependency_overrides[get_db] = db_returning([
        make_row("Padang; Barus", "pelayaran"),  # urutan terbalik di input
    ])
    try:
        data = (await _get("/api/research/network-pelabuhan")).json()
        assert len(data["edges"]) == 1
        assert data["edges"][0]["source"] == "Barus"
        assert data["edges"][0]["target"] == "Padang"
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_three_ports_make_three_pairs():
    """N port di satu baris -> C(N,2) pasangan. 3 port -> 3 edge."""
    app.dependency_overrides[get_db] = db_returning([
        make_row("Barus; Inderapura; Padang", "sengketa"),
    ])
    try:
        data = (await _get("/api/research/network-pelabuhan")).json()
        assert len(data["edges"]) == 3
        assert _edge(data, "Barus", "Inderapura")["weight"] == 1
        assert _edge(data, "Barus", "Padang")["weight"] == 1
        assert _edge(data, "Inderapura", "Padang")["weight"] == 1
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_edge_weight_accumulates():
    """Pasangan yang sama di banyak baris -> bobot bertambah."""
    app.dependency_overrides[get_db] = db_returning([
        make_row("Barus; Padang", "syahbandar"),
        make_row("Barus; Padang", "syahbandar"),
        make_row("Padang; Barus", "pelayaran"),
    ])
    try:
        data = (await _get("/api/research/network-pelabuhan")).json()
        e = _edge(data, "Barus", "Padang")
        assert e["weight"] == 3
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_node_weight_is_mention_count():
    """Bobot node = jumlah baris yang menyebut pelabuhan itu (bukan derajat edge)."""
    app.dependency_overrides[get_db] = db_returning([
        make_row("Padang", "syahbandar"),          # solo mention
        make_row("Barus; Padang", "pelayaran"),    # Padang lagi + Barus
    ])
    try:
        data = (await _get("/api/research/network-pelabuhan")).json()
        assert _node(data, "Padang")["weight"] == 2
        assert _node(data, "Barus")["weight"] == 1
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_edge_tema_is_modal_with_breakdown():
    """tema edge = tema modal antar baris pembentuk; tema_breakdown merinci komposisi."""
    app.dependency_overrides[get_db] = db_returning([
        make_row("Barus; Padang", "syahbandar"),
        make_row("Barus; Padang", "syahbandar"),
        make_row("Barus; Padang", "pelayaran"),
    ])
    try:
        data = (await _get("/api/research/network-pelabuhan")).json()
        e = _edge(data, "Barus", "Padang")
        assert e["tema"] == "syahbandar"  # 2 vs 1
        assert e["tema_breakdown"] == {"syahbandar": 2, "pelayaran": 1}
    finally:
        app.dependency_overrides.clear()


# ─── Edge cases ──────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_unknown_port_excluded():
    """'Tidak diketahui' bukan entitas: tak jadi node maupun edge."""
    app.dependency_overrides[get_db] = db_returning([
        make_row("Tidak diketahui", "syahbandar"),
        make_row("Tidak diketahui; Padang", "pelayaran"),
    ])
    try:
        data = (await _get("/api/research/network-pelabuhan")).json()
        assert _node(data, "Tidak diketahui") is None
        assert _node(data, "Padang") is not None
        # baris kedua cuma sisakan 1 port nyata -> tak ada edge
        assert data["edges"] == []
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_single_port_no_edge():
    """Baris satu pelabuhan -> node ada, tak ada edge."""
    app.dependency_overrides[get_db] = db_returning([
        make_row("Padang", "syahbandar"),
    ])
    try:
        data = (await _get("/api/research/network-pelabuhan")).json()
        assert _node(data, "Padang") is not None
        assert data["edges"] == []
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_empty_result():
    """Tak ada baris -> {nodes:[], edges:[], meta}."""
    app.dependency_overrides[get_db] = db_returning([])
    try:
        data = (await _get("/api/research/network-pelabuhan")).json()
        assert data["nodes"] == []
        assert data["edges"] == []
        assert data["meta"]["n_edges"] == 0
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_year_params_accepted():
    """Param year_from/year_to diterima (filter NULL-inclusive di SQL, di-verify via curl)."""
    app.dependency_overrides[get_db] = db_returning([
        make_row("Barus; Padang", "syahbandar", dekade=1660, tahun=1668),
    ])
    try:
        r = await _get("/api/research/network-pelabuhan?year_from=1660&year_to=1699")
        assert r.status_code == 200
        assert _edge(r.json(), "Barus", "Padang") is not None
    finally:
        app.dependency_overrides.clear()


# ─── Scope PRD penuh: field label + filter tema ──────────────────────────────

@pytest.mark.asyncio
async def test_node_has_label_equal_to_id():
    """Kontrak PRD nodes:{id,label,weight}. Utk pelabuhan, label (display) = id."""
    app.dependency_overrides[get_db] = db_returning([
        make_row("Barus; Padang", "syahbandar"),
    ])
    try:
        data = (await _get("/api/research/network-pelabuhan")).json()
        assert data["nodes"], "harus ada node"
        for n in data["nodes"]:
            assert n["label"] == n["id"]
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_tema_filter_keeps_only_matching_rows():
    """?tema=X: hanya baris tema X membentuk graf; pasangan/port tema lain hilang."""
    app.dependency_overrides[get_db] = db_returning([
        make_row("Barus; Padang", "syahbandar"),
        make_row("Barus; Inderapura", "pelayaran"),
    ])
    try:
        data = (await _get("/api/research/network-pelabuhan?tema=syahbandar")).json()
        assert _edge(data, "Barus", "Padang") is not None
        assert _edge(data, "Barus", "Inderapura") is None
        assert _node(data, "Inderapura") is None   # cuma muncul di baris pelayaran
        assert _node(data, "Padang") is not None
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_tema_filter_no_match_empty():
    """?tema=<tak ada di data>: graf kosong, meta konsisten."""
    app.dependency_overrides[get_db] = db_returning([
        make_row("Barus; Padang", "syahbandar"),
    ])
    try:
        data = (await _get("/api/research/network-pelabuhan?tema=tidak_ada")).json()
        assert data["nodes"] == []
        assert data["edges"] == []
        assert data["meta"]["n_edges"] == 0
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_deterministic_ordering():
    """Node urut by id, edge urut by (source,target) — output stabil (cache-friendly)."""
    app.dependency_overrides[get_db] = db_returning([
        make_row("Padang; Barus; Inderapura", "syahbandar"),
    ])
    try:
        data = (await _get("/api/research/network-pelabuhan")).json()
        node_ids = [n["id"] for n in data["nodes"]]
        assert node_ids == sorted(node_ids)
        edge_keys = [(e["source"], e["target"]) for e in data["edges"]]
        assert edge_keys == sorted(edge_keys)
    finally:
        app.dependency_overrides.clear()
