"""
Unit tests for /api/voyages endpoints.
Uses FastAPI dependency override with mock DB session.
Follows the same proven pattern as test_forts.py.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from httpx import AsyncClient, ASGITransport
from types import SimpleNamespace

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app


# ─── Fixtures ────────────────────────────────────────────────────────────────

def make_voyage(**kwargs):
    defaults = {
        "id": 1,
        "voyage_ref": 13447,
        "origin_id": 1,
        "destination_id": 6,
        "origin_name_raw": "Padang",
        "destination_name_raw": "Batavia",
        "ship_name": "Theeboom",
        "captain": "Jan de Vries",
        "tonnage": None,
        "year": 1700,
        "departure_date": None,
        "arrival_date": "1700-12-08",
        "total_gulden": 98358.05,
        "main_product": "goud",
        "all_products": "goud | peper | kamfer",
        "cargo_count": 26,
        "destination": "Batavia",
        "duration_days": 44,
        "direction": "outbound",
        "source_url": "https://resources.huygens.knaw.nl/bgb/voyage/13447",
    }
    defaults.update(kwargs)
    return SimpleNamespace(**defaults)


VOYAGE_OUTBOUND_1 = make_voyage(id=1, ship_name="Theeboom", direction="outbound", year=1700)
VOYAGE_OUTBOUND_2 = make_voyage(id=2, ship_name="Wind", direction="outbound", year=1701, total_gulden=18338.58)
VOYAGE_INBOUND_1  = make_voyage(id=3, ship_name="Batavia Retour", direction="inbound", year=1702, 
                                origin_name_raw="Batavia", destination_name_raw="Padang",
                                origin_id=6, destination_id=1)
VOYAGE_TRANSIT_1  = make_voyage(id=4, ship_name="Palembang Trader", direction="transit", year=1705,
                                origin_name_raw="Palembang", destination_name_raw="Batavia",
                                origin_id=7, destination_id=6)


def make_scalar_result(items):
    mock = MagicMock()
    mock.scalars.return_value.all.return_value = items
    mock.scalar_one_or_none.return_value = items[0] if items else None
    return mock


# ─── Tests: GET /api/voyages/ ────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_list_voyages_returns_list():
    """GET /api/voyages/ should return a list of voyages."""
    async def mock_get_db():
        session = AsyncMock()
        session.execute.return_value = make_scalar_result(
            [VOYAGE_OUTBOUND_1, VOYAGE_OUTBOUND_2]
        )
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/voyages/")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2


@pytest.mark.asyncio
async def test_list_voyages_has_direction_field():
    """Each voyage should include the direction field."""
    async def mock_get_db():
        session = AsyncMock()
        session.execute.return_value = make_scalar_result([VOYAGE_OUTBOUND_1, VOYAGE_INBOUND_1])
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/voyages/")

    app.dependency_overrides.clear()

    data = response.json()
    assert len(data) == 2
    directions = {d["ship_name"]: d["direction"] for d in data}
    assert directions["Theeboom"] == "outbound"
    assert directions["Batavia Retour"] == "inbound"


@pytest.mark.asyncio
async def test_list_voyages_has_new_fields():
    """Voyages should expose departure_date, arrival_date, cargo_count."""
    async def mock_get_db():
        session = AsyncMock()
        session.execute.return_value = make_scalar_result([VOYAGE_OUTBOUND_1])
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/voyages/")

    app.dependency_overrides.clear()

    data = response.json()
    assert len(data) == 1
    voyage = data[0]
    assert "direction" in voyage
    assert "arrival_date" in voyage
    assert "departure_date" in voyage
    assert "cargo_count" in voyage
    assert voyage["arrival_date"] == "1700-12-08"
    assert voyage["cargo_count"] == 26


# ─── Tests: GET /api/voyages/{id} ────────────────────────────────────────────

@pytest.mark.asyncio
async def test_get_voyage_detail():
    """GET /api/voyages/1 should return voyage details."""
    async def mock_get_db():
        session = AsyncMock()
        session.execute.return_value = make_scalar_result([VOYAGE_OUTBOUND_1])
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/voyages/1")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert data["ship_name"] == "Theeboom"
    assert data["direction"] == "outbound"
    assert data["total_gulden"] == 98358.05


@pytest.mark.asyncio
async def test_get_voyage_not_found():
    """GET /api/voyages/9999 should return 404."""
    async def mock_get_db():
        session = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        session.execute.return_value = mock_result
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/voyages/9999")

    app.dependency_overrides.clear()

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


# ─── Tests: Direction filtering ──────────────────────────────────────────────

@pytest.mark.asyncio
async def test_filter_outbound_voyages():
    """GET /api/voyages/?direction=outbound should only return outbound voyages."""
    async def mock_get_db():
        session = AsyncMock()
        # Mock returns only outbound when filtered
        session.execute.return_value = make_scalar_result([VOYAGE_OUTBOUND_1, VOYAGE_OUTBOUND_2])
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/voyages/?direction=outbound")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert all(v["direction"] == "outbound" for v in data)


@pytest.mark.asyncio
async def test_filter_inbound_voyages():
    """GET /api/voyages/?direction=inbound should only return inbound voyages."""
    async def mock_get_db():
        session = AsyncMock()
        session.execute.return_value = make_scalar_result([VOYAGE_INBOUND_1])
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/voyages/?direction=inbound")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["direction"] == "inbound"
    assert data[0]["ship_name"] == "Batavia Retour"


# ─── Tests: Year range filtering ─────────────────────────────────────────────

@pytest.mark.asyncio
async def test_filter_by_year_range():
    """GET /api/voyages/?year_from=1701&year_to=1705 should filter correctly."""
    async def mock_get_db():
        session = AsyncMock()
        session.execute.return_value = make_scalar_result([VOYAGE_OUTBOUND_2, VOYAGE_INBOUND_1])
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/voyages/?year_from=1701&year_to=1705")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    years = [v["year"] for v in data]
    assert all(1701 <= y <= 1705 for y in years)
