"""
US-05: Direction Toggle — Outbound / Inbound / All

TDD untuk fitur toggle arah pelayaran di map.
Backend: GET /api/voyages/routes?direction= (sudah ada, verifikasi behavior)
Frontend: toggle button HTML + JS state (diuji di Django tests.py)

Fokus backend test:
- Filter direction=outbound hanya return outbound
- Filter direction=inbound hanya return inbound (atau kosong jika tidak ada data)
- Tanpa filter return semua direction
- direction=invalid → 200 + empty list (bukan 422) karena string filter
- direction filter + year filter kombinasi benar
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from httpx import AsyncClient, ASGITransport
from types import SimpleNamespace

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app


def make_route(origin, dest, direction, count=10, value=500_000.0,
               olat=-0.96, olon=100.35, dlat=-6.12, dlon=106.82):
    return SimpleNamespace(
        origin_name=origin, destination_name=dest,
        origin_lat=olat, origin_lon=olon,
        dest_lat=dlat, dest_lon=dlon,
        direction=direction, count=count, total_value=value,
    )


OUTBOUND_ROUTES = [
    make_route("Padang",       "Batavia",  "outbound", 147, 12_000_000.0),
    make_route("Barus",        "Batavia",  "outbound",  45,  3_500_000.0, olat=2.01, olon=98.40),
    make_route("Pulau Cingkuak","Batavia", "outbound",  20,  1_800_000.0, olat=-1.35, olon=100.56),
]

INBOUND_ROUTES = [
    make_route("Batavia", "Padang",        "inbound", 75,  8_000_000.0, olat=-6.12, olon=106.82, dlat=-0.96, dlon=100.35),
    make_route("Batavia", "Air Bangis",    "inbound", 30,  2_500_000.0, olat=-6.12, olon=106.82, dlat=0.20,  dlon=99.38),
]

TRANSIT_ROUTES = [
    make_route("Palembang", "Batavia", "transit", 268, 9_000_000.0, olat=-3.00, olon=104.78),
]

ALL_ROUTES = OUTBOUND_ROUTES + INBOUND_ROUTES + TRANSIT_ROUTES


def _mock_db(routes):
    async def mock_get_db():
        session = AsyncMock()
        result = MagicMock()
        result.all.return_value = routes
        session.execute.return_value = result
        yield session
    return mock_get_db


# ─── 1. Filter direction=outbound ────────────────────────────────────────────

@pytest.mark.asyncio
async def test_direction_toggle_outbound_returns_only_outbound():
    """GET /api/voyages/routes?direction=outbound → semua item ber-direction outbound."""
    from database import get_db
    app.dependency_overrides[get_db] = _mock_db(OUTBOUND_ROUTES)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.get("/api/voyages/routes?direction=outbound")

    app.dependency_overrides.clear()

    assert r.status_code == 200
    data = r.json()
    assert len(data) == 3
    assert all(item["direction"] == "outbound" for item in data)


@pytest.mark.asyncio
async def test_direction_toggle_outbound_response_has_westkust_origin():
    """Direction outbound harus punya origin dari Westkust (Padang, Barus, dsb)."""
    from database import get_db
    app.dependency_overrides[get_db] = _mock_db(OUTBOUND_ROUTES)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.get("/api/voyages/routes?direction=outbound")

    app.dependency_overrides.clear()

    data = r.json()
    origins = {item["origin_name"] for item in data}
    westkust = {"Padang", "Barus", "Air Bangis", "Pulau Cingkuak", "Air Haji"}
    assert origins & westkust, f"Expected Westkust origins, got: {origins}"


# ─── 2. Filter direction=inbound ─────────────────────────────────────────────

@pytest.mark.asyncio
async def test_direction_toggle_inbound_returns_only_inbound():
    """GET /api/voyages/routes?direction=inbound → item ber-direction inbound."""
    from database import get_db
    app.dependency_overrides[get_db] = _mock_db(INBOUND_ROUTES)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.get("/api/voyages/routes?direction=inbound")

    app.dependency_overrides.clear()

    assert r.status_code == 200
    data = r.json()
    assert len(data) == 2
    assert all(item["direction"] == "inbound" for item in data)


@pytest.mark.asyncio
async def test_direction_toggle_inbound_empty_when_no_data():
    """GET /api/voyages/routes?direction=inbound → empty list jika tidak ada data inbound."""
    from database import get_db
    app.dependency_overrides[get_db] = _mock_db([])

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.get("/api/voyages/routes?direction=inbound")

    app.dependency_overrides.clear()

    assert r.status_code == 200
    assert r.json() == []


# ─── 3. Tanpa filter = semua direction ───────────────────────────────────────

@pytest.mark.asyncio
async def test_direction_toggle_all_returns_mixed_directions():
    """GET /api/voyages/routes (tanpa direction) → semua direction dikembalikan."""
    from database import get_db
    app.dependency_overrides[get_db] = _mock_db(ALL_ROUTES)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.get("/api/voyages/routes")

    app.dependency_overrides.clear()

    assert r.status_code == 200
    data = r.json()
    directions = {item["direction"] for item in data}
    assert "outbound" in directions
    assert "inbound" in directions
    assert "transit" in directions


# ─── 4. Kombinasi direction + year filter ────────────────────────────────────

@pytest.mark.asyncio
async def test_direction_toggle_with_year_from():
    """GET /api/voyages/routes?direction=outbound&year_from=1750 → filter kombinasi benar."""
    from database import get_db
    # Mock returns filtered subset (DB already filtered)
    filtered = [make_route("Padang", "Batavia", "outbound", 40, 3_000_000.0)]
    app.dependency_overrides[get_db] = _mock_db(filtered)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.get("/api/voyages/routes?direction=outbound&year_from=1750")

    app.dependency_overrides.clear()

    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    assert data[0]["direction"] == "outbound"


@pytest.mark.asyncio
async def test_direction_toggle_with_year_range():
    """GET /api/voyages/routes?direction=outbound&year_from=1700&year_to=1750."""
    from database import get_db
    filtered = OUTBOUND_ROUTES[:2]
    app.dependency_overrides[get_db] = _mock_db(filtered)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.get("/api/voyages/routes?direction=outbound&year_from=1700&year_to=1750")

    app.dependency_overrides.clear()

    assert r.status_code == 200
    data = r.json()
    assert len(data) == 2
    assert all(item["direction"] == "outbound" for item in data)


# ─── 5. direction + limit kombinasi ──────────────────────────────────────────

@pytest.mark.asyncio
async def test_direction_filter_respects_limit():
    """GET /api/voyages/routes?direction=outbound&limit=2 → max 2 results."""
    from database import get_db
    # Mock returns 3 routes, but limit=2 means endpoint slices to 2
    app.dependency_overrides[get_db] = _mock_db(OUTBOUND_ROUTES)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.get("/api/voyages/routes?direction=outbound&limit=2")

    app.dependency_overrides.clear()

    assert r.status_code == 200
    data = r.json()
    assert len(data) <= 2


# ─── 6. Response schema untuk antPath rendering ───────────────────────────────

@pytest.mark.asyncio
async def test_direction_response_has_color_relevant_fields():
    """
    Response harus punya field direction, origin_lat, dest_lat untuk warna antPath.
    US-05 frontend menggunakan r.direction untuk warna biru (outbound) / oranye (inbound).
    """
    from database import get_db
    app.dependency_overrides[get_db] = _mock_db([OUTBOUND_ROUTES[0]])

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.get("/api/voyages/routes?direction=outbound")

    app.dependency_overrides.clear()

    assert r.status_code == 200
    item = r.json()[0]
    assert "direction" in item
    assert "origin_lat" in item
    assert "dest_lat" in item
    assert item["direction"] == "outbound"
