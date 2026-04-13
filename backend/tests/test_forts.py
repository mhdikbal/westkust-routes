"""
Unit tests for /api/forts endpoints.
Uses FastAPI dependency override with mock DB session.
Voyage/Fort mock objects use SimpleNamespace to give Pydantic v2 real attribute access.

Tests updated for:
- port_type field on Fort
- duration_days in VoyageBrief
- New ports (Air Bangis, Barus, Lampung, etc.)
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

def make_fort(id, name, latitude, longitude, color, description,
              port_type="departure"):
    return SimpleNamespace(
        id=id, name=name, latitude=latitude,
        longitude=longitude, color=color, description=description,
        port_type=port_type,
    )

def make_voyage(id, fort_id, ship_name, captain, year, total_gulden,
                main_product, all_products, destination, duration_days, source_url,
                direction="outbound", departure_date=None, arrival_date=None, cargo_count=None,
                origin_id=None, destination_id=None, origin_name_raw=None, destination_name_raw=None):
    return SimpleNamespace(
        id=id, fort_id=fort_id, ship_name=ship_name, captain=captain,
        year=year, total_gulden=total_gulden, main_product=main_product,
        all_products=all_products, destination=destination,
        duration_days=duration_days, source_url=source_url,
        direction=direction, departure_date=departure_date,
        arrival_date=arrival_date, cargo_count=cargo_count,
        origin_id=origin_id or fort_id, destination_id=destination_id,
        origin_name_raw=origin_name_raw, destination_name_raw=destination_name_raw,
    )


# ─── Mock data ────────────────────────────────────────────────────────────────

MOCK_FORT_PADANG    = make_fort(1, "Padang",      -0.9655545, 100.3538895,
                                "#c0392b", "Fort Padang desc", port_type="both")
MOCK_FORT_CINGKUAK  = make_fort(2, "Pulau Cingkuak", -1.352837, 100.559995,
                                "#e67e22", "Fort Cingkuak desc", port_type="departure")
MOCK_FORT_AIRHAJI   = make_fort(3, "Air Haji",    -1.933939, 100.866982,
                                "#27ae60", "Fort Air Haji desc", port_type="departure")
MOCK_FORT_AIRBANGIS = make_fort(4, "Air Bangis",   0.197487,  99.375555,
                                "#2980b9", "Air Bangis desc",    port_type="departure")
MOCK_FORT_BARUS     = make_fort(5, "Barus",         2.014457,  98.399320,
                                "#16a085", "Barus desc",         port_type="departure")
MOCK_FORT_BATAVIA   = make_fort(6, "Batavia",     -6.1165019, 106.8165122,
                                "#2c3e50", "Fort Batavia desc",  port_type="arrival")
MOCK_FORT_JAMBI     = make_fort(7, "Jambi",        -1.098448, 104.175718,
                                "#d35400", "Jambi desc",         port_type="arrival")
MOCK_FORT_LAMPUNG   = make_fort(8, "Lampung",      -5.357800, 105.280387,
                                "#7f8c8d", "Lampung desc",       port_type="arrival")

ALL_MOCK_FORTS = [
    MOCK_FORT_PADANG, MOCK_FORT_CINGKUAK, MOCK_FORT_AIRHAJI,
    MOCK_FORT_AIRBANGIS, MOCK_FORT_BARUS, MOCK_FORT_BATAVIA,
    MOCK_FORT_JAMBI, MOCK_FORT_LAMPUNG,
]

MOCK_VOYAGE_1 = make_voyage(1, 1, "Theeboom", "Jan de Vries", 1700, 98358.05,
    "goud", "goud | peper | kamfer", "Batavia", 44,
    "https://resources.huygens.knaw.nl/bgb/voyage/13447")

MOCK_VOYAGE_2 = make_voyage(2, 1, "Wind", None, 1701, 18338.58,
    "peper", "peper | kamfer", "Batavia", 38,
    "https://resources.huygens.knaw.nl/bgb/voyage/13448")

MOCK_VOYAGE_3 = make_voyage(3, 5, "Binnendijk", "Pieter Koot", 1720, 55000.0,
    "kamfer", "kamfer | benzoin", "Batavia", 62,
    "https://resources.huygens.knaw.nl/bgb/voyage/99001")


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
    """GET /api/forts/ should return a list of all forts including new ports."""
    async def mock_get_db():
        session = AsyncMock()
        session.execute.side_effect = [
            make_scalar_result(ALL_MOCK_FORTS),
            # Stats per fort (Outbound and Inbound for 8 forts)
            *[MagicMock(one=MagicMock(return_value=(10, 500000.0)))
              for _ in range(len(ALL_MOCK_FORTS) * 2)],
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
async def test_list_forts_contains_port_type():
    """GET /api/forts/ should include port_type field for each fort."""
    async def mock_get_db():
        session = AsyncMock()
        session.execute.side_effect = [
            make_scalar_result([MOCK_FORT_PADANG, MOCK_FORT_BATAVIA]),
            MagicMock(one=MagicMock(return_value=(5, 100000.0))), # Outbound Padang
            MagicMock(one=MagicMock(return_value=(1, 10000.0))),  # Inbound Padang
            MagicMock(one=MagicMock(return_value=(2, 50000.0))),  # Outbound Batavia
            MagicMock(one=MagicMock(return_value=(3, 20000.0))),  # Inbound Batavia
        ]
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/forts/")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    port_types = {d["name"]: d["port_type"] for d in data}
    assert port_types["Padang"]  == "both"
    assert port_types["Batavia"] == "arrival"


@pytest.mark.asyncio
async def test_list_forts_departure_ports_present():
    """New departure ports (Air Bangis, Barus) should be in the list."""
    async def mock_get_db():
        session = AsyncMock()
        session.execute.side_effect = [
            make_scalar_result(ALL_MOCK_FORTS),
            *[MagicMock(one=MagicMock(return_value=(0, 0.0)))
              for _ in range(len(ALL_MOCK_FORTS) * 2)],
        ]
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/forts/")

    app.dependency_overrides.clear()

    names = [d["name"] for d in response.json()]
    assert "Air Bangis" in names
    assert "Barus"      in names
    assert "Lampung"    in names


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
    """GET /api/forts/1 should return fort detail with voyages and port_type."""
    async def mock_get_db():
        session = AsyncMock()

        fort_result = MagicMock()
        fort_result.scalar_one_or_none.return_value = MOCK_FORT_PADANG

        voyages_result = MagicMock()
        voyages_result.scalars.return_value.all.return_value = [MOCK_VOYAGE_1, MOCK_VOYAGE_2]

        inbound_voyages_result = MagicMock()
        inbound_voyages_result.scalars.return_value.all.return_value = []

        out_stats_result = MagicMock()
        out_stats_result.one.return_value = (2, 116696.63, 1700, 1701)

        in_stats_result = MagicMock()
        in_stats_result.one.return_value = (0, 0.0, None, None)

        session.execute.side_effect = [
            fort_result, voyages_result, inbound_voyages_result,
            out_stats_result, in_stats_result
        ]
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/forts/1")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert data["name"]      == "Padang"
    assert data["port_type"] == "both"
    assert data["latitude"]  == pytest.approx(-0.9655545, rel=1e-4)
    assert data["longitude"] == pytest.approx(100.3538895, rel=1e-4)
    assert "outbound_voyages" in data
    assert len(data["outbound_voyages"]) == 2


@pytest.mark.asyncio
async def test_voyage_has_duration_days():
    """Voyage in fort detail should expose duration_days field."""
    async def mock_get_db():
        session = AsyncMock()
        fort_result = MagicMock()
        fort_result.scalar_one_or_none.return_value = MOCK_FORT_PADANG
        voyages_result = MagicMock()
        voyages_result.scalars.return_value.all.return_value = [MOCK_VOYAGE_1]
        
        inbound_voyages_result = MagicMock()
        inbound_voyages_result.scalars.return_value.all.return_value = []
        
        out_stats_result = MagicMock()
        out_stats_result.one.return_value = (1, 98358.05, 1700, 1700)
        
        in_stats_result = MagicMock()
        in_stats_result.one.return_value = (0, 0.0, None, None)
        
        session.execute.side_effect = [
            fort_result, voyages_result, inbound_voyages_result,
            out_stats_result, in_stats_result
        ]
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/forts/1")

    app.dependency_overrides.clear()

    data = response.json()
    assert "duration_days" in data["outbound_voyages"][0]
    assert data["outbound_voyages"][0]["duration_days"] == 44


@pytest.mark.asyncio
async def test_get_fort_barus_departure():
    """GET /api/forts/5 should return Barus as departure port."""
    async def mock_get_db():
        session = AsyncMock()
        fort_result = MagicMock()
        fort_result.scalar_one_or_none.return_value = MOCK_FORT_BARUS
        voyages_result = MagicMock()
        voyages_result.scalars.return_value.all.return_value = [MOCK_VOYAGE_3]

        inbound_voyages_result = MagicMock()
        inbound_voyages_result.scalars.return_value.all.return_value = []

        out_stats_result = MagicMock()
        out_stats_result.one.return_value = (1, 55000.0, 1720, 1720)

        in_stats_result = MagicMock()
        in_stats_result.one.return_value = (0, 0.0, None, None)

        session.execute.side_effect = [
            fort_result, voyages_result, inbound_voyages_result,
            out_stats_result, in_stats_result
        ]
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/forts/5")

    app.dependency_overrides.clear()

    data = response.json()
    assert data["name"]      == "Barus"
    assert data["port_type"] == "departure"
    assert data["outbound_voyages"][0]["duration_days"] == 62


@pytest.mark.asyncio
async def test_list_fort_voyages():
    """GET /api/forts/1/voyages should return voyage list."""
    async def mock_get_db():
        session = AsyncMock()
        fort_result = MagicMock()
        fort_result.scalar_one_or_none.return_value = MOCK_FORT_PADANG
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
    assert "Wind"     in ship_names


@pytest.mark.asyncio
async def test_list_fort_voyages_filter_year():
    """GET /api/forts/1/voyages?year_from=1700&year_to=1700 should filter correctly."""
    async def mock_get_db():
        session = AsyncMock()
        fort_result = MagicMock()
        fort_result.scalar_one_or_none.return_value = MOCK_FORT_PADANG
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
    assert data[0]["year"]      == 1700
