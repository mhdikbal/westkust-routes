"""
Unit tests untuk GET /api/research/linimasa.
Pola mock DB session dari test_research_atjeh_trade.py.
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


def make_row(**overrides):
    base = dict(
        id=1, source_document="1637", source_page=99, book_page="86",
        event_date_raw="10-12 Maret 1637", year=1637, event_type="suksesi",
        ruler_actor="Coninck van Atchijn", title="Raja Atjeh wafat",
        era_slug="klaim-awal",
        text_asli="de anachoda van de joncgen rapporteert dat den coninck van Atchijn overleden is",
        confidence_flag="unverified", notes=None,
    )
    base.update(overrides)
    return SimpleNamespace(**base)


def make_scalar_result(items):
    mock = MagicMock()
    mock.scalars.return_value.all.return_value = items
    return mock


def db_returning(rows):
    async def mock_get_db():
        session = AsyncMock()
        session.execute.return_value = make_scalar_result(rows)
        yield session
    return mock_get_db


async def _get(url):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        return await client.get(url)


@pytest.mark.asyncio
async def test_returns_items_and_meta():
    app.dependency_overrides[get_db] = db_returning([
        make_row(id=1, event_type="suksesi", year=1637),
        make_row(id=2, event_type="perjanjian", year=1663),
    ])
    try:
        r = await _get("/api/research/linimasa")
        assert r.status_code == 200
        data = r.json()
        assert len(data["items"]) == 2
        assert data["meta"]["n_items"] == 2
        assert data["meta"]["by_event_type"] == {"suksesi": 1, "perjanjian": 1}
        assert data["meta"]["year_min"] == 1637
        assert data["meta"]["year_max"] == 1663
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_item_shape_preserves_title_and_text_asli():
    app.dependency_overrides[get_db] = db_returning([
        make_row(id=1, title="Traktat Painan", text_asli="1º diluaskan..."),
    ])
    try:
        r = await _get("/api/research/linimasa")
        data = r.json()
        assert data["items"][0]["title"] == "Traktat Painan"
        assert data["items"][0]["text_asli"]
        assert data["items"][0]["confidence_flag"] == "unverified"
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_empty_result_ok():
    app.dependency_overrides[get_db] = db_returning([])
    try:
        r = await _get("/api/research/linimasa")
        assert r.status_code == 200
        data = r.json()
        assert data["items"] == []
        assert data["meta"]["n_items"] == 0
        assert data["meta"]["year_min"] is None
        assert data["meta"]["year_max"] is None
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_event_type_query_param_accepted():
    app.dependency_overrides[get_db] = db_returning([
        make_row(id=1, event_type="perjanjian"),
    ])
    try:
        r = await _get("/api/research/linimasa?event_type=perjanjian")
        assert r.status_code == 200
        data = r.json()
        assert all(item["event_type"] == "perjanjian" for item in data["items"])
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_year_from_year_to_query_params_accepted():
    """year_from/year_to harus diterima FastAPI tanpa 422 (query dibangun, DB di-mock)."""
    app.dependency_overrides[get_db] = db_returning([
        make_row(id=1, year=1663),
    ])
    try:
        r = await _get("/api/research/linimasa?year_from=1660&year_to=1665")
        assert r.status_code == 200
        data = r.json()
        assert len(data["items"]) == 1
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_era_slug_passthrough():
    """Fase 1 /linimasa (SSR + narasi berbab): era_slug wajib ikut ke response,
    dipakai Django view utk kelompokkan event per babak sebelum di-render."""
    app.dependency_overrides[get_db] = db_returning([
        make_row(id=1, era_slug="retak-painan", title="Traktat Painan"),
    ])
    try:
        r = await _get("/api/research/linimasa")
        data = r.json()
        assert data["items"][0]["era_slug"] == "retak-painan"
    finally:
        app.dependency_overrides.clear()
