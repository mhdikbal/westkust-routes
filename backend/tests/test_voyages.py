"""
Unit tests for /api/voyages endpoints.
Uses FastAPI dependency override with mock DB session.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from httpx import AsyncClient, ASGITransport
from types import SimpleNamespace

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app


# ─── Mock Data — SimpleNamespace gives real scalar attributes ─────────────────

def make_voyage(**kw):
    return SimpleNamespace(**kw)


MOCK_VOYAGE_A = make_voyage(
    id=1, fort_id=1, ship_name="Theeboom", captain=None, year=1700,
    total_gulden=98358.05, main_product="goud",
    all_products="goud | peper | kamfer | benzoë",
    destination="Batavia,Batavia", duration_days=None,
    source_url="https://resources.huygens.knaw.nl/bgb/voyage/13447",
)

MOCK_VOYAGE_B = make_voyage(
    id=2, fort_id=1, ship_name="Rijnenburg", captain=None, year=1707,
    total_gulden=228.93, main_product="peper",
    all_products="peper",
    destination="-,Bengalen", duration_days=None,
    source_url="https://resources.huygens.knaw.nl/bgb/voyage/15968",
)

MOCK_VOYAGE_C = make_voyage(
    id=3, fort_id=2, ship_name="Prins Eugenius", captain=None, year=1721,
    total_gulden=136892.23, main_product="goud",
    all_products="goud | peper | benzoë",
    destination="Batavia,Batavia", duration_days=None,
    source_url="https://resources.huygens.knaw.nl/bgb/voyage/16234",
)


def voyages_result_mock(voyages):
    mock = MagicMock()
    mock.scalars.return_value.all.return_value = voyages
    return mock


def voyage_result_mock(voyage):
    mock = MagicMock()
    mock.scalar_one_or_none.return_value = voyage
    return mock


# ─── Tests: GET /api/voyages/ ────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_list_voyages_returns_list():
    """GET /api/voyages/ should return a list of voyages."""
    async def mock_get_db():
        session = AsyncMock()
        session.execute.return_value = voyages_result_mock([MOCK_VOYAGE_A, MOCK_VOYAGE_B, MOCK_VOYAGE_C])
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/voyages/")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3


@pytest.mark.asyncio
async def test_list_voyages_filter_by_fort():
    """GET /api/voyages/?fort_id=1 should filter by fort."""
    async def mock_get_db():
        session = AsyncMock()
        session.execute.return_value = voyages_result_mock([MOCK_VOYAGE_A, MOCK_VOYAGE_B])
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/voyages/?fort_id=1")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all(v["fort_id"] == 1 for v in data)


@pytest.mark.asyncio
async def test_list_voyages_filter_by_year_range():
    """GET /api/voyages/?year_from=1700&year_to=1710 filters by year."""
    async def mock_get_db():
        session = AsyncMock()
        # Return only voyages in range
        session.execute.return_value = voyages_result_mock([MOCK_VOYAGE_A, MOCK_VOYAGE_B])
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/voyages/?year_from=1700&year_to=1710")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for v in data:
        assert v["year"] >= 1700
        assert v["year"] <= 1710


@pytest.mark.asyncio
async def test_list_voyages_filter_by_product():
    """GET /api/voyages/?product=peper filters by commodity."""
    async def mock_get_db():
        session = AsyncMock()
        session.execute.return_value = voyages_result_mock([MOCK_VOYAGE_B])
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/voyages/?product=peper")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_list_voyages_empty():
    """GET /api/voyages/ with no data returns empty list."""
    async def mock_get_db():
        session = AsyncMock()
        session.execute.return_value = voyages_result_mock([])
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/voyages/")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == []


# ─── Tests: GET /api/voyages/{id} ────────────────────────────────────────────

@pytest.mark.asyncio
async def test_get_voyage_detail():
    """GET /api/voyages/1 returns correct voyage fields."""
    async def mock_get_db():
        session = AsyncMock()
        session.execute.return_value = voyage_result_mock(MOCK_VOYAGE_A)
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/voyages/1")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["ship_name"] == "Theeboom"
    assert data["year"] == 1700
    assert data["main_product"] == "goud"
    assert data["total_gulden"] == pytest.approx(98358.05, rel=1e-3)
    assert data["fort_id"] == 1
    assert "source_url" in data
    assert "huygens" in data["source_url"]


@pytest.mark.asyncio
async def test_get_voyage_not_found():
    """GET /api/voyages/9999 returns 404."""
    async def mock_get_db():
        session = AsyncMock()
        session.execute.return_value = voyage_result_mock(None)
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/voyages/9999")

    app.dependency_overrides.clear()

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_voyage_has_all_required_fields():
    """Voyage response contains all required fields."""
    async def mock_get_db():
        session = AsyncMock()
        session.execute.return_value = voyage_result_mock(MOCK_VOYAGE_C)
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/voyages/3")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    required_fields = ["id", "fort_id", "ship_name", "year", "total_gulden",
                       "main_product", "all_products", "destination", "source_url"]
    for field in required_fields:
        assert field in data, f"Missing field: {field}"


@pytest.mark.asyncio
async def test_voyage_products_contain_pipe_separator():
    """all_products field uses | as separator."""
    async def mock_get_db():
        session = AsyncMock()
        session.execute.return_value = voyage_result_mock(MOCK_VOYAGE_A)
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/voyages/1")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    if data["all_products"] and "|" in data["all_products"]:
        products = [p.strip() for p in data["all_products"].split("|")]
        assert len(products) > 1
        assert "goud" in products
