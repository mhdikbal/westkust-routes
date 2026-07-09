"""
SNK-2 — Unit tests untuk GET /api/research/sankey-tema.
TDD: ditulis SEBELUM implementasi (docs/sprint-sankey-tema-korpus.md).

Sankey 3-tingkat: dekade -> tema_dominan -> pelabuhan (multi-port di-explode).
Reuse SankeyResponse ({nodes:[{name}], links:[{source,target,value}]}).
Pakai FastAPI dependency override + mock DB session (pola test_voyages.py).
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


def make_row(dekade, tema, pelabuhan, tahun=None):
    """Satu baris research_theme_rows sebagaimana dikembalikan query agregasi."""
    if tahun is None and dekade is not None:
        tahun = dekade  # cukup utk filter test
    return SimpleNamespace(
        dekade=dekade, tema_dominan=tema, pelabuhan_disebut=pelabuhan, tahun=tahun
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


def _node_index(data):
    return {n["name"]: i for i, n in enumerate(data["nodes"])}


# ─── Happy path ──────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_sankey_basic_structure():
    """Struktur {nodes, links}; node dekade+tema+pelabuhan ada; link 2 tingkat."""
    rows = [
        make_row(1660, "syahbandar", "Padang"),
        make_row(1660, "syahbandar", "Barus"),
        make_row(1670, "pelayaran", "Padang"),
    ]
    app.dependency_overrides[get_db] = db_returning(rows)
    try:
        resp = await _get("/api/research/sankey-tema")
    finally:
        app.dependency_overrides.clear()

    assert resp.status_code == 200
    data = resp.json()
    names = {n["name"] for n in data["nodes"]}
    # tiga tingkat hadir
    assert {"1660", "1670", "syahbandar", "pelayaran", "Padang", "Barus"} <= names
    assert len(data["links"]) > 0
    # semua indeks link valid
    for lk in data["links"]:
        assert 0 <= lk["source"] < len(data["nodes"])
        assert 0 <= lk["target"] < len(data["nodes"])


@pytest.mark.asyncio
async def test_sankey_flow_conservation():
    """Konservasi: total aliran dekade->tema == total tema->pelabuhan."""
    rows = [
        make_row(1660, "syahbandar", "Padang"),
        make_row(1660, "syahbandar", "Barus"),
        make_row(1670, "pelayaran", "Padang"),
    ]
    app.dependency_overrides[get_db] = db_returning(rows)
    try:
        data = (await _get("/api/research/sankey-tema")).json()
    finally:
        app.dependency_overrides.clear()

    idx = _node_index(data)
    temas = {"syahbandar", "pelayaran"}
    tema_idx = {idx[t] for t in temas if t in idx}
    into_tema = sum(lk["value"] for lk in data["links"] if lk["target"] in tema_idx)
    out_of_tema = sum(lk["value"] for lk in data["links"] if lk["source"] in tema_idx)
    assert into_tema == out_of_tema == 3


# ─── Multi-port explode (FIX #2 / PRD P0 AC #2) ──────────────────────────────

@pytest.mark.asyncio
async def test_sankey_multiport_explode():
    """Baris multi-pelabuhan -> N link tema->pelabuhan terpisah (bukan node gabungan)."""
    rows = [make_row(1730, "syahbandar", "Barus; Padang; Pariaman")]
    app.dependency_overrides[get_db] = db_returning(rows)
    try:
        data = (await _get("/api/research/sankey-tema")).json()
    finally:
        app.dependency_overrides.clear()

    names = {n["name"] for n in data["nodes"]}
    # tidak ada node gabungan ";"
    assert not any(";" in n for n in names)
    assert {"Barus", "Padang", "Pariaman"} <= names
    idx = _node_index(data)
    syah = idx["syahbandar"]
    out_ports = {n["name"]: lk["value"]
                 for lk in data["links"] if lk["source"] == syah
                 for n in [data["nodes"][lk["target"]]]}
    assert out_ports == {"Barus": 1, "Padang": 1, "Pariaman": 1}


# ─── Filter tahun ────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_sankey_year_filter_passthrough():
    """year_from/year_to diterima (200) dan hanya baris cocok yg diagregasi.

    Filter tahun sesungguhnya dilakukan di SQL WHERE; di sini kita hanya memastikan
    endpoint menerima param & tetap mengagregasi baris yg dikembalikan DB.
    """
    rows = [make_row(1670, "pelayaran", "Padang", tahun=1672)]
    app.dependency_overrides[get_db] = db_returning(rows)
    try:
        resp = await _get("/api/research/sankey-tema?year_from=1660&year_to=1680")
    finally:
        app.dependency_overrides.clear()
    assert resp.status_code == 200
    data = resp.json()
    assert {"1670", "pelayaran", "Padang"} <= {n["name"] for n in data["nodes"]}


# ─── Edge: NULL dekade & kosong ──────────────────────────────────────────────

@pytest.mark.asyncio
async def test_sankey_null_dekade_bucket():
    """Baris dekade NULL -> node 'Tak bertahun' (tidak di-drop diam-diam)."""
    rows = [make_row(None, "sengketa", "Pariaman")]
    app.dependency_overrides[get_db] = db_returning(rows)
    try:
        data = (await _get("/api/research/sankey-tema")).json()
    finally:
        app.dependency_overrides.clear()
    assert "Tak bertahun" in {n["name"] for n in data["nodes"]}


@pytest.mark.asyncio
async def test_sankey_empty_is_200_not_500():
    """Nol baris -> {nodes:[], links:[]} dengan 200 (bukan 500)."""
    app.dependency_overrides[get_db] = db_returning([])
    try:
        resp = await _get("/api/research/sankey-tema")
    finally:
        app.dependency_overrides.clear()
    assert resp.status_code == 200
    assert resp.json() == {"nodes": [], "links": []}
