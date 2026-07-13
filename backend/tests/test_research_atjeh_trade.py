"""
Unit tests untuk GET /api/research/atjeh-trade.
TDD: ditulis SEBELUM implementasi endpoint (mengekspos atjeh_trade_records,
lihat backend/tests/test_atjeh_trade.py utk asal datanya).
Pola mock DB session dari test_voyages.py (result.scalars().all()).
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
        id=1, source_page=137, book_page="120", entry_date_raw="9 Mei 1644",
        direction="in_atjeh", commodity_raw="peper", quantity_raw="22", unit_raw="bhaer",
        price_value=7.0, price_unit_raw="theijl/bhaer",
        actor_raw="ondercoopman Jan Lucassen Levendich",
        text_asli="22 bhaer peeper ende 18 catti tegens 7 theijl de bhaer genegotieert",
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
        make_row(id=1, direction="in_atjeh"),
        make_row(id=2, direction="van_atjeh", commodity_raw="benjuwin"),
    ])
    try:
        r = await _get("/api/research/atjeh-trade")
        assert r.status_code == 200
        data = r.json()
        assert len(data["items"]) == 2
        assert data["meta"]["n_items"] == 2
        assert data["meta"]["by_direction"] == {"in_atjeh": 1, "van_atjeh": 1}
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_item_shape_preserves_original_terms():
    """commodity_raw hrs lolos apa adanya (tak diterjemahkan) sampai ke response JSON."""
    app.dependency_overrides[get_db] = db_returning([
        make_row(id=1, commodity_raw="salpeter"),
    ])
    try:
        r = await _get("/api/research/atjeh-trade")
        data = r.json()
        assert data["items"][0]["commodity_raw"] == "salpeter"
        assert data["items"][0]["confidence_flag"] == "unverified"
        assert data["items"][0]["text_asli"]
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_empty_result_ok():
    app.dependency_overrides[get_db] = db_returning([])
    try:
        r = await _get("/api/research/atjeh-trade")
        assert r.status_code == 200
        data = r.json()
        assert data["items"] == []
        assert data["meta"]["n_items"] == 0
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_direction_query_param_accepted():
    """direction=naar_atjeh harus diterima FastAPI tanpa 422 (query dibangun, DB di-mock)."""
    app.dependency_overrides[get_db] = db_returning([
        make_row(id=3, direction="naar_atjeh"),
    ])
    try:
        r = await _get("/api/research/atjeh-trade?direction=naar_atjeh")
        assert r.status_code == 200
        data = r.json()
        assert all(item["direction"] == "naar_atjeh" for item in data["items"])
    finally:
        app.dependency_overrides.clear()
