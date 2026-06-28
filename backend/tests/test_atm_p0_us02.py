"""
US-02: Fort AMH Enrichment Endpoint

TDD RED phase — GET /api/forts/{id}/enrichment belum ada.
Test ini akan FAIL sampai endpoint diimplementasikan.

Setelah endpoint ada → semua test harus PASS (GREEN).

Pola mock: AsyncMock + SimpleNamespace (sama dengan test_forts.py).
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from httpx import AsyncClient, ASGITransport
from types import SimpleNamespace

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app


# ─── Helpers ─────────────────────────────────────────────────────────────────

def make_fort_enriched(
    id=1,
    name="Padang",
    latitude=-0.966,
    longitude=100.354,
    color="#c0392b",
    description="Pusat perdagangan VOC di Pantai Barat Sumatra",
    port_type="both",
    nama_historis="Padangh",
    designasi_voc="Sumatras Westcust (VOC-gebied)",
    fungsi_historis="Markas komandan perdagangan Pantai Barat Sumatra",
    periode_aktif=None,
    amh_url="https://www.atlasofmutualheritage.nl/page/5751/padang",
    amh_images=None,
):
    """Create a Fort SimpleNamespace with all enrichment fields."""
    return SimpleNamespace(
        id=id,
        name=name,
        latitude=latitude,
        longitude=longitude,
        color=color,
        description=description,
        port_type=port_type,
        nama_historis=nama_historis,
        designasi_voc=designasi_voc,
        fungsi_historis=fungsi_historis,
        periode_aktif=periode_aktif,
        amh_url=amh_url,
        amh_images=amh_images,
    )


MOCK_FORT_PADANG = make_fort_enriched()

MOCK_FORT_NO_AMH = make_fort_enriched(
    id=2,
    name="Air Bangis",
    latitude=0.197,
    longitude=99.375,
    color="#2980b9",
    description="Pelabuhan Air Bangis",
    port_type="departure",
    nama_historis="Air Bangis",
    designasi_voc="Handelshaven",
    fungsi_historis="Pos perdagangan lada dan kamfer",
    amh_url=None,
)


def _mock_db_found(fort):
    """Return a mock DB session for the enrichment endpoint.

    The endpoint makes 3 execute() calls:
      1. select(Fort) → scalar_one_or_none() returns fort
      2. select(count, sum) outbound → one() returns (count, total)
      3. select(count, sum) inbound  → one() returns (count, total)
    """
    async def mock_get_db():
        session = AsyncMock()

        fort_result = MagicMock()
        fort_result.scalar_one_or_none.return_value = fort

        stats_result = MagicMock()
        stats_result.one.return_value = (0, 0.0)

        session.execute.side_effect = [fort_result, stats_result, stats_result]
        yield session
    return mock_get_db


def _mock_db_not_found():
    """Return a mock DB session that yields None (fort not found)."""
    async def mock_get_db():
        session = AsyncMock()
        result = MagicMock()
        result.scalar_one_or_none.return_value = None
        session.execute.return_value = result
        yield session
    return mock_get_db


# ─── Tests: GET /api/forts/{id}/enrichment ───────────────────────────────────

@pytest.mark.asyncio
async def test_enrichment_endpoint_returns_200():
    """GET /api/forts/1/enrichment harus return HTTP 200."""
    from database import get_db
    app.dependency_overrides[get_db] = _mock_db_found(MOCK_FORT_PADANG)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/forts/1/enrichment")

    app.dependency_overrides.clear()

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_enrichment_returns_nama_historis():
    """Response harus mengandung field 'nama_historis'."""
    from database import get_db
    app.dependency_overrides[get_db] = _mock_db_found(MOCK_FORT_PADANG)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/forts/1/enrichment")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert "nama_historis" in data
    assert data["nama_historis"] == "Padangh"


@pytest.mark.asyncio
async def test_enrichment_returns_designasi_voc():
    """Response harus mengandung field 'designasi_voc'."""
    from database import get_db
    app.dependency_overrides[get_db] = _mock_db_found(MOCK_FORT_PADANG)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/forts/1/enrichment")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert "designasi_voc" in data
    assert data["designasi_voc"] == "Sumatras Westcust (VOC-gebied)"


@pytest.mark.asyncio
async def test_enrichment_returns_fungsi_historis():
    """Response harus mengandung field 'fungsi_historis'."""
    from database import get_db
    app.dependency_overrides[get_db] = _mock_db_found(MOCK_FORT_PADANG)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/forts/1/enrichment")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert "fungsi_historis" in data
    assert data["fungsi_historis"] == "Markas komandan perdagangan Pantai Barat Sumatra"


@pytest.mark.asyncio
async def test_enrichment_returns_amh_url():
    """Response harus mengandung field 'amh_url' dengan nilai yang benar."""
    from database import get_db
    app.dependency_overrides[get_db] = _mock_db_found(MOCK_FORT_PADANG)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/forts/1/enrichment")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert "amh_url" in data
    assert data["amh_url"] == "https://www.atlasofmutualheritage.nl/page/5751/padang"


@pytest.mark.asyncio
async def test_enrichment_amh_url_null_not_omitted():
    """Jika amh_url=None → response harus ada field 'amh_url' bernilai null, bukan field hilang."""
    from database import get_db
    app.dependency_overrides[get_db] = _mock_db_found(MOCK_FORT_NO_AMH)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/forts/2/enrichment")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    # Field harus ada meskipun nilainya null
    assert "amh_url" in data
    assert data["amh_url"] is None


@pytest.mark.asyncio
async def test_enrichment_fort_not_found_returns_404():
    """GET /api/forts/9999/enrichment harus return 404 jika fort tidak ada."""
    from database import get_db
    app.dependency_overrides[get_db] = _mock_db_not_found()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/forts/9999/enrichment")

    app.dependency_overrides.clear()

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_enrichment_does_not_break_existing_detail():
    """
    GET /api/forts/1 (existing endpoint) harus masih return 200.
    Backward-compatibility: endpoint enrichment tidak boleh break /api/forts/{id}.
    """
    async def mock_get_db():
        session = AsyncMock()

        fort_result = MagicMock()
        fort_result.scalar_one_or_none.return_value = MOCK_FORT_PADANG

        voyages_result = MagicMock()
        voyages_result.scalars.return_value.all.return_value = []

        inbound_voyages_result = MagicMock()
        inbound_voyages_result.scalars.return_value.all.return_value = []

        out_stats_result = MagicMock()
        out_stats_result.one.return_value = (0, 0.0, None, None)

        in_stats_result = MagicMock()
        in_stats_result.one.return_value = (0, 0.0, None, None)

        session.execute.side_effect = [
            fort_result,
            voyages_result,
            inbound_voyages_result,
            out_stats_result,
            in_stats_result,
        ]
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/forts/1")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Padang"
    assert "outbound_voyages" in data
    assert "inbound_voyages" in data


# ─── Tests: US-10 AMH Gallery — amh_images field ─────────────────────────────

MOCK_FORT_WITH_AMH_IMAGES = make_fort_enriched(
    id=1,
    name="Padang",
    amh_url="https://www.atlasofmutualheritage.nl/page/5751/padang",
    amh_images=[
        {
            "title": "Kaart Westkust",
            "creator": "VOC",
            "year": "1780",
            "thumbnail_url": None,
            "page_url": "https://www.atlasofmutualheritage.nl/page/5751/padang",
        }
    ],
)


@pytest.mark.asyncio
async def test_enrichment_returns_amh_images_field():
    """GET /api/forts/{id}/enrichment harus punya key 'amh_images' di response (boleh null atau list)."""
    from database import get_db
    app.dependency_overrides[get_db] = _mock_db_found(MOCK_FORT_WITH_AMH_IMAGES)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/forts/1/enrichment")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert "amh_images" in data, "Field 'amh_images' harus ada di response enrichment"


@pytest.mark.asyncio
async def test_enrichment_amh_images_list_or_null():
    """Nilai amh_images harus list atau null — bukan tipe lain (int, str, bool, dll.)."""
    from database import get_db
    app.dependency_overrides[get_db] = _mock_db_found(MOCK_FORT_WITH_AMH_IMAGES)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/forts/1/enrichment")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    value = data.get("amh_images")
    assert value is None or isinstance(value, list), (
        f"amh_images harus bertipe list atau null, dapat: {type(value).__name__}"
    )
