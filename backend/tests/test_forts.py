"""
Unit tests for /api/forts endpoints.
Uses FastAPI dependency override with mock DB session.
Voyage/Fort mock objects use SimpleNamespace to give Pydantic v2 real attribute access.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from httpx import AsyncClient, ASGITransport
from types import SimpleNamespace

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app


# ─── Fixtures — use SimpleNamespace so Pydantic gets real Python scalars ─────

def make_fort(id, name, latitude, longitude, color, description):
    return SimpleNamespace(
        id=id, name=name, latitude=latitude,
        longitude=longitude, color=color, description=description,
    )

def make_voyage(id, fort_id, ship_name, captain, year, total_gulden,
                main_product, all_products, destination, duration_days, source_url):
    return SimpleNamespace(
        id=id, fort_id=fort_id, ship_name=ship_name, captain=captain,
        year=year, total_gulden=total_gulden, main_product=main_product,
        all_products=all_products, destination=destination,
        duration_days=duration_days, source_url=source_url,
    )


MOCK_FORT_1 = make_fort(1, "Padang", -0.9655545, 100.3538895, "#c0392b", "Fort Padang description")
MOCK_FORT_2 = make_fort(2, "Batavia", -6.1165019, 106.8165122, "#8e44ad", "Fort Batavia description")

MOCK_VOYAGE_1 = make_voyage(1, 1, "Theeboom", None, 1700, 98358.05,
    "goud", "goud | peper | kamfer", "Batavia,Batavia", None,
    "https://resources.huygens.knaw.nl/bgb/voyage/13447")

MOCK_VOYAGE_2 = make_voyage(2, 1, "Wind", None, 1700, 18338.58,
    "goud", "goud | kamfer", "Batavia,Batavia", None,
    "https://resources.huygens.knaw.nl/bgb/voyage/13448")


def make_scalar_result(items):
    mock = MagicMock()
    mock.scalars.return_value.all.return_value = items
    mock.scalar_one_or_none.return_value = items[0] if items else None
    mock.scalar_one.return_value = items[0] if items else None
    total_gulden = sum(getattr(v, "total_gulden", None) or 0 for v in items)
    mock.one.return_value = (len(items), total_gulden, 1700, 1750)
    return mock


# ─── Tests: GET /api/forts/ ──────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_list_forts_returns_list():
    """GET /api/forts/ should return a list of forts."""
    async def mock_get_db():
        session = AsyncMock()
        # First call: list forts
        session.execute.side_effect = [
            make_scalar_result([MOCK_FORT_1, MOCK_FORT_2]),
            # Stats for fort 1
            MagicMock(one=MagicMock(return_value=(10, 500000.0))),
            # Stats for fort 2
            MagicMock(one=MagicMock(return_value=(5, 250000.0))),
        ]
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/forts/")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_health_endpoint():
    """GET /api/health should return status ok."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "service" in body


@pytest.mark.asyncio
async def test_get_fort_not_found():
    """GET /api/forts/9999 should return 404."""
    async def mock_get_db():
        session = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        session.execute.return_value = mock_result
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/forts/9999")

    app.dependency_overrides.clear()

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_get_fort_detail():
    """GET /api/forts/1 should return fort detail with voyages."""
    async def mock_get_db():
        session = AsyncMock()

        fort_result = MagicMock()
        fort_result.scalar_one_or_none.return_value = MOCK_FORT_1

        voyages_result = MagicMock()
        voyages_result.scalars.return_value.all.return_value = [MOCK_VOYAGE_1, MOCK_VOYAGE_2]

        stats_result = MagicMock()
        stats_result.one.return_value = (2, 116696.63, 1700, 1700)

        session.execute.side_effect = [fort_result, voyages_result, stats_result]
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/forts/1")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Padang"
    assert data["latitude"] == pytest.approx(-0.9655545, rel=1e-4)
    assert data["longitude"] == pytest.approx(100.3538895, rel=1e-4)
    assert data["color"] == "#c0392b"
    assert "voyages" in data
    assert isinstance(data["voyages"], list)
    assert len(data["voyages"]) == 2


@pytest.mark.asyncio
async def test_list_fort_voyages():
    """GET /api/forts/1/voyages should return voyage list."""
    async def mock_get_db():
        session = AsyncMock()

        fort_result = MagicMock()
        fort_result.scalar_one_or_none.return_value = MOCK_FORT_1

        voyages_result = MagicMock()
        voyages_result.scalars.return_value.all.return_value = [MOCK_VOYAGE_1, MOCK_VOYAGE_2]

        session.execute.side_effect = [fort_result, voyages_result]
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/forts/1/voyages")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    ship_names = [v["ship_name"] for v in data]
    assert "Theeboom" in ship_names
    assert "Wind" in ship_names


@pytest.mark.asyncio
async def test_list_fort_voyages_filter_year():
    """GET /api/forts/1/voyages?year_from=1700&year_to=1700 should filter correctly."""
    async def mock_get_db():
        session = AsyncMock()

        fort_result = MagicMock()
        fort_result.scalar_one_or_none.return_value = MOCK_FORT_1

        voyages_result = MagicMock()
        voyages_result.scalars.return_value.all.return_value = [MOCK_VOYAGE_1]

        session.execute.side_effect = [fort_result, voyages_result]
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/forts/1/voyages?year_from=1700&year_to=1700")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["ship_name"] == "Theeboom"
    assert data[0]["year"] == 1700
