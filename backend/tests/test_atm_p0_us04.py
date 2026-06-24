"""
US-04 — Limit Parameter for /api/voyages/routes
Sprint ATM P0 | Tim Jangkar QA

TDD: Tests 1, 2, 3, 8 start RED (limit param not yet on endpoint).
     Tests 4, 5, 6, 7 start GREEN (direction filter + schema already work).

Run:
    docker compose exec backend pytest tests/test_atm_p0_us04.py -v
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from httpx import AsyncClient, ASGITransport
from types import SimpleNamespace

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app


# ─── Helper ──────────────────────────────────────────────────────────────────

def make_route_row(
    origin_name, destination_name, direction, count, total_value,
    origin_lat=-0.96, origin_lon=100.35, dest_lat=-6.12, dest_lon=106.82,
):
    return SimpleNamespace(
        origin_name=origin_name,
        destination_name=destination_name,
        origin_lat=origin_lat,
        origin_lon=origin_lon,
        dest_lat=dest_lat,
        dest_lon=dest_lon,
        direction=direction,
        count=count,
        total_value=total_value,
    )


def _make_60_routes():
    """Return 60 synthetic route rows for limit-cap tests."""
    origins = ["Padang", "Barus", "Air Bangis", "Pulau Cingkuak", "Air Haji"]
    return [
        make_route_row(
            origin_name=origins[i % len(origins)],
            destination_name="Batavia",
            direction="outbound",
            count=i + 1,
            total_value=float((i + 1) * 10_000),
        )
        for i in range(60)
    ]


# ═══════════════════════════════════════════════════════════════════════════════
#  RED tests — require `limit` parameter on endpoint (not yet implemented)
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_routes_limit_default_returns_50_max():
    """
    RED: GET /api/voyages/routes without explicit limit → mock returns 60 rows →
    endpoint MUST cap response at 50.  Will FAIL until limit=50 default is added.
    """
    sixty_rows = _make_60_routes()

    async def mock_get_db():
        session = AsyncMock()
        result = MagicMock()
        result.all.return_value = sixty_rows
        session.execute.return_value = result
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.get("/api/voyages/routes")

    app.dependency_overrides.clear()

    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) <= 50, (
        f"Expected at most 50 routes (default cap), got {len(data)}. "
        "Add `limit: int = 50` to get_voyage_routes and slice `routes[:limit]`."
    )


@pytest.mark.asyncio
async def test_routes_limit_param_respected():
    """
    RED: GET /api/voyages/routes?limit=5 → mock returns 60 rows →
    endpoint MUST honour limit=5 and return exactly 5 items.
    """
    sixty_rows = _make_60_routes()

    async def mock_get_db():
        session = AsyncMock()
        result = MagicMock()
        result.all.return_value = sixty_rows
        session.execute.return_value = result
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.get("/api/voyages/routes?limit=5")

    app.dependency_overrides.clear()

    assert r.status_code == 200
    data = r.json()
    assert len(data) == 5, (
        f"Expected exactly 5 routes with limit=5, got {len(data)}."
    )


@pytest.mark.asyncio
async def test_routes_limit_25_returns_25():
    """
    RED: GET /api/voyages/routes?limit=25 → mock returns 60 rows →
    endpoint must return exactly 25.
    """
    sixty_rows = _make_60_routes()

    async def mock_get_db():
        session = AsyncMock()
        result = MagicMock()
        result.all.return_value = sixty_rows
        session.execute.return_value = result
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.get("/api/voyages/routes?limit=25")

    app.dependency_overrides.clear()

    assert r.status_code == 200
    data = r.json()
    assert len(data) == 25, (
        f"Expected exactly 25 routes with limit=25, got {len(data)}."
    )


@pytest.mark.asyncio
async def test_routes_limit_invalid_returns_422():
    """
    RED: GET /api/voyages/routes?limit=abc → must return 422 Unprocessable Entity.
    FastAPI validates `limit: int`; will FAIL until the parameter is declared.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.get("/api/voyages/routes?limit=abc")

    assert r.status_code == 422, (
        f"Expected 422 for non-integer limit, got {r.status_code}. "
        "Declare `limit: int = 50` on the endpoint so FastAPI validates it."
    )


# ═══════════════════════════════════════════════════════════════════════════════
#  GREEN tests — direction filter + schema already work today
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_routes_direction_filter_outbound():
    """
    GREEN: GET /api/voyages/routes?direction=outbound → all returned items have
    direction == 'outbound'.  (direction filter already exists on endpoint.)
    """
    async def mock_get_db():
        session = AsyncMock()
        result = MagicMock()
        result.all.return_value = [
            make_route_row("Padang",       "Batavia", "outbound", 45, 1_500_000.0),
            make_route_row("Barus",        "Batavia", "outbound", 12,   400_000.0,
                           origin_lat=2.01, origin_lon=98.40),
            make_route_row("Air Bangis",   "Batavia", "outbound",  8,   250_000.0,
                           origin_lat=0.20, origin_lon=99.38),
        ]
        session.execute.return_value = result
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.get("/api/voyages/routes?direction=outbound")

    app.dependency_overrides.clear()

    assert r.status_code == 200
    data = r.json()
    assert len(data) > 0
    for item in data:
        assert item["direction"] == "outbound", (
            f"Expected direction='outbound', got '{item['direction']}'"
        )


@pytest.mark.asyncio
async def test_routes_direction_filter_transit():
    """
    GREEN: GET /api/voyages/routes?direction=transit → all returned items have
    direction == 'transit'.
    """
    async def mock_get_db():
        session = AsyncMock()
        result = MagicMock()
        result.all.return_value = [
            make_route_row("Jambi", "Batavia", "transit", 7, 180_000.0,
                           origin_lat=-1.10, origin_lon=104.18),
        ]
        session.execute.return_value = result
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.get("/api/voyages/routes?direction=transit")

    app.dependency_overrides.clear()

    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    assert data[0]["direction"] == "transit"


@pytest.mark.asyncio
async def test_routes_has_lat_lon_coordinates():
    """
    GREEN: Each route item must expose origin_lat, origin_lon, dest_lat, dest_lon
    so that the Leaflet antPath renderer can place the polyline correctly.
    """
    async def mock_get_db():
        session = AsyncMock()
        result = MagicMock()
        result.all.return_value = [
            make_route_row(
                "Padang", "Batavia", "outbound", 30, 900_000.0,
                origin_lat=-0.966, origin_lon=100.354,
                dest_lat=-6.117, dest_lon=106.817,
            ),
        ]
        session.execute.return_value = result
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.get("/api/voyages/routes")

    app.dependency_overrides.clear()

    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    item = data[0]
    coord_fields = {"origin_lat", "origin_lon", "dest_lat", "dest_lon"}
    assert coord_fields.issubset(set(item.keys())), (
        f"Missing coordinate fields: {coord_fields - set(item.keys())}"
    )
    assert item["origin_lat"] == pytest.approx(-0.966, rel=1e-3)
    assert item["origin_lon"] == pytest.approx(100.354, rel=1e-3)
    assert item["dest_lat"]   == pytest.approx(-6.117, rel=1e-3)
    assert item["dest_lon"]   == pytest.approx(106.817, rel=1e-3)


@pytest.mark.asyncio
async def test_routes_has_required_fields_for_antpath():
    """
    GREEN: Each route item must expose origin_name, destination_name, count,
    total_value — the four fields consumed by drawRoutes() in the Leaflet frontend.
    """
    async def mock_get_db():
        session = AsyncMock()
        result = MagicMock()
        result.all.return_value = [
            make_route_row("Pulau Cingkuak", "Batavia", "outbound", 18, 600_000.0,
                           origin_lat=-1.353, origin_lon=100.560),
            make_route_row("Batavia", "Padang", "inbound", 5, 100_000.0,
                           origin_lat=-6.117, origin_lon=106.817,
                           dest_lat=-0.966, dest_lon=100.354),
        ]
        session.execute.return_value = result
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.get("/api/voyages/routes")

    app.dependency_overrides.clear()

    assert r.status_code == 200
    data = r.json()
    assert len(data) == 2

    required_fields = {"origin_name", "destination_name", "count", "total_value"}
    for item in data:
        assert required_fields.issubset(set(item.keys())), (
            f"Missing antPath fields: {required_fields - set(item.keys())}"
        )

    # Spot-check values
    first = data[0]
    assert first["origin_name"] == "Pulau Cingkuak"
    assert first["destination_name"] == "Batavia"
    assert first["count"] == 18
    assert first["total_value"] == pytest.approx(600_000.0, rel=1e-3)
