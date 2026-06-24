"""
US-01: BGB Link-Through per Voyage — TDD Contract Tests

Memverifikasi bahwa:
1. GET /api/voyages/ mengembalikan field source_url di setiap voyage
2. source_url null dikembalikan sebagai null (bukan dihapus dari response)
3. GET /api/forts/{id} voyage briefs juga mengekspos source_url
4. source_url yang ada harus berasal dari domain BGB Huygens yang benar

Ekspektasi: semua test PASS langsung (source_url sudah ada di model & schema).
Jika ada yang FAIL → itu regresi nyata, fix dulu sebelum lanjut sprint.
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

BGB_URL = "https://resources.huygens.knaw.nl/bgb/voyage/13447"

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
        "year": 1726,
        "departure_date": "1726-03-10",
        "arrival_date": "1726-04-23",
        "total_gulden": 98358.05,
        "main_product": "goud",
        "all_products": "goud | peper | kamfer",
        "cargo_count": 26,
        "destination": "Batavia",
        "duration_days": 44,
        "direction": "outbound",
        "source_url": BGB_URL,
    }
    defaults.update(kwargs)
    return SimpleNamespace(**defaults)


def make_fort(**kwargs):
    defaults = {
        "id": 1,
        "name": "Padang",
        "latitude": -0.9655545,
        "longitude": 100.3538895,
        "color": "#c0392b",
        "description": "Fort Padang",
        "port_type": "both",
    }
    defaults.update(kwargs)
    return SimpleNamespace(**defaults)


def make_scalar_result(items):
    mock = MagicMock()
    mock.scalars.return_value.all.return_value = items
    mock.scalar_one_or_none.return_value = items[0] if items else None
    return mock


def make_one_result(value):
    mock = MagicMock()
    mock.one.return_value = (value, value, value, value)
    mock.scalar.return_value = value
    mock.scalars.return_value.all.return_value = [value] if value else []
    return mock


# ─── Tests: source_url di /api/voyages/ ──────────────────────────────────────

@pytest.mark.asyncio
async def test_voyage_list_exposes_source_url():
    """GET /api/voyages/ harus mengembalikan source_url di setiap item."""
    voyage = make_voyage(source_url=BGB_URL)

    async def mock_get_db():
        session = AsyncMock()
        session.execute.return_value = make_scalar_result([voyage])
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/voyages/")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert "source_url" in data[0], "source_url harus ada di response voyage list"
    assert data[0]["source_url"] == BGB_URL


@pytest.mark.asyncio
async def test_voyage_list_source_url_null_when_absent():
    """Voyage tanpa source_url harus mengembalikan null, bukan field yang dihilangkan."""
    voyage = make_voyage(source_url=None)

    async def mock_get_db():
        session = AsyncMock()
        session.execute.return_value = make_scalar_result([voyage])
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/voyages/")

    app.dependency_overrides.clear()

    data = response.json()
    assert len(data) == 1
    assert "source_url" in data[0], "source_url harus tetap ada di response meski null"
    assert data[0]["source_url"] is None


@pytest.mark.asyncio
async def test_voyage_single_exposes_source_url():
    """GET /api/voyages/{id} harus mengembalikan source_url."""
    voyage = make_voyage(id=99, source_url=BGB_URL)

    async def mock_get_db():
        session = AsyncMock()
        session.execute.return_value = make_scalar_result([voyage])
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/voyages/99")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert "source_url" in data
    assert data["source_url"] == BGB_URL


# ─── Tests: source_url di /api/forts/{id} voyage briefs ──────────────────────

@pytest.mark.asyncio
async def test_fort_detail_voyage_brief_exposes_source_url():
    """VoyageBrief di GET /api/forts/{id} harus menyertakan source_url."""
    fort = make_fort(id=1)
    voyage_out = make_voyage(id=10, origin_id=1, destination_id=6, source_url=BGB_URL)
    voyage_in  = make_voyage(id=11, origin_id=6, destination_id=1, direction="inbound",
                              source_url="https://resources.huygens.knaw.nl/bgb/voyage/11000")

    async def mock_get_db():
        session = AsyncMock()

        def execute_side_effect(query):
            q = str(query)
            if "forts" in q.lower() and "where" in q.lower():
                return make_scalar_result([fort])
            # outbound voyages
            r = MagicMock()
            r.scalars.return_value.all.return_value = [voyage_out]
            r.one.return_value = (1, 98358.05, 1726, 1726)
            r.scalar.return_value = 1
            return r

        session.execute.side_effect = execute_side_effect
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/forts/1")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert "outbound_voyages" in data
    if data["outbound_voyages"]:
        brief = data["outbound_voyages"][0]
        assert "source_url" in brief, "VoyageBrief di fort detail harus ekspos source_url"


# ─── Security: validasi prefix domain BGB ────────────────────────────────────

@pytest.mark.asyncio
async def test_source_url_is_bgb_domain():
    """source_url yang dikembalikan harus berasal dari domain BGB Huygens."""
    ALLOWED_PREFIX = "https://resources.huygens.knaw.nl"

    voyage = make_voyage(source_url=BGB_URL)

    async def mock_get_db():
        session = AsyncMock()
        session.execute.return_value = make_scalar_result([voyage])
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/voyages/")

    app.dependency_overrides.clear()

    data = response.json()
    for voyage_item in data:
        if voyage_item["source_url"]:
            assert voyage_item["source_url"].startswith(ALLOWED_PREFIX), (
                f"source_url harus domain BGB Huygens, dapat: {voyage_item['source_url']}"
            )


@pytest.mark.asyncio
async def test_source_url_present_in_mixed_list():
    """List voyage campuran (ada dan tidak ada source_url) harus konsisten."""
    v_with_url    = make_voyage(id=1, source_url=BGB_URL)
    v_without_url = make_voyage(id=2, source_url=None, ship_name="Ghost Ship")

    async def mock_get_db():
        session = AsyncMock()
        session.execute.return_value = make_scalar_result([v_with_url, v_without_url])
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/voyages/")

    app.dependency_overrides.clear()

    data = response.json()
    assert len(data) == 2
    url_map = {d["ship_name"]: d["source_url"] for d in data}
    assert url_map["Theeboom"] == BGB_URL
    assert url_map["Ghost Ship"] is None
