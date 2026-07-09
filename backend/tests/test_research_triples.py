"""
SNK-5 — Unit tests untuk GET /api/research/sankey-tema/triples.
Agregasi (dekade, tema, pelabuhan) -> [n, n_lowconf] + meta, dipakai halaman
Django /riset/tema (render Sankey + filter tahun client-side).
Pola: dependency override + mock DB (.all()) seperti test_research_sankey.py.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from httpx import AsyncClient, ASGITransport
from types import SimpleNamespace
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from database import get_db


def make_row(dekade, tema, pelabuhan, low=False, asal="daghregister"):
    return SimpleNamespace(
        dekade=dekade, tema_dominan=tema, pelabuhan_disebut=pelabuhan,
        low_confidence=low, corpus_asal=asal,
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


@pytest.mark.asyncio
async def test_triples_aggregation_and_multiport_explode():
    """Baris multi-port di-explode; triple yang sama dijumlahkan; low-conf terpisah."""
    rows = [
        make_row(1660, "syahbandar", "Padang"),
        make_row(1660, "syahbandar", "Padang", low=True),
        make_row(1660, "syahbandar", "Barus; Padang"),  # explode -> 2 kontribusi
    ]
    app.dependency_overrides[get_db] = db_returning(rows)
    try:
        resp = await _get("/api/research/sankey-tema/triples")
    finally:
        app.dependency_overrides.clear()
    assert resp.status_code == 200
    d = resp.json()
    trip = {(t[0], t[1], t[2]): (t[3], t[4]) for t in d["triples"]}
    # (1660, syahbandar, Padang): 3 kontribusi (row1 + row2 + explode row3), 1 low
    assert trip[(1660, "syahbandar", "Padang")] == [3, 1] or trip[(1660, "syahbandar", "Padang")] == (3, 1)
    assert trip[(1660, "syahbandar", "Barus")][0] == 1
    # kontribusi total = 4 (1 + 1 + 2)
    assert d["meta"]["contrib"] == 4


@pytest.mark.asyncio
async def test_triples_meta_counts():
    """meta: total baris, split korpus, low-conf, dekade, tema."""
    rows = [
        make_row(1660, "syahbandar", "Padang", asal="daghregister"),
        make_row(1670, "pelayaran", "Barus", asal="globalise"),
        make_row(None, "sengketa", "Salido", low=True, asal="globalise"),  # tak bertahun
    ]
    app.dependency_overrides[get_db] = db_returning(rows)
    try:
        resp = await _get("/api/research/sankey-tema/triples")
    finally:
        app.dependency_overrides.clear()
    m = resp.json()["meta"]
    assert m["total"] == 3
    assert m["n_dagh"] == 1
    assert m["n_glob"] == 2
    assert m["n_lowconf"] == 1
    assert m["decades"] == [1660, 1670]      # None tidak masuk daftar dekade
    assert set(m["temas"]) == {"syahbandar", "pelayaran", "sengketa"}
    assert m["n_ports"] == 3


@pytest.mark.asyncio
async def test_triples_null_dekade_preserved():
    """Baris dekade NULL tetap jadi triple (dek=None), tidak di-drop."""
    rows = [make_row(None, "syahbandar", "Padang")]
    app.dependency_overrides[get_db] = db_returning(rows)
    try:
        resp = await _get("/api/research/sankey-tema/triples")
    finally:
        app.dependency_overrides.clear()
    d = resp.json()
    assert d["triples"][0][0] is None
    assert d["meta"]["contrib"] == 1
