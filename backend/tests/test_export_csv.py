"""
CSV Export tests — US-19 Sprint PROD-RISET

Verifikasi endpoint GET /api/voyages/export:
- Return status 200 dengan Content-Type: text/csv
- Content-Disposition: attachment; filename=voyages_westkust.csv
- Baris pertama adalah header CSV
- Data voyage tersedia di baris berikutnya
- Filter year_from, year_to, direction bekerja

Mock pattern sama dengan test_voyages.py (AsyncMock + dependency override).
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from httpx import AsyncClient, ASGITransport
from types import SimpleNamespace
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app

CSV_HEADERS = [
    "voyage_ref", "ship_name", "captain", "year",
    "departure_date", "arrival_date", "origin_name_raw",
    "destination_name_raw", "direction", "main_product",
    "all_products", "total_gulden", "cargo_count",
    "duration_days", "source_url",
]


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
        "year": 1720,
        "departure_date": "1720-03-01",
        "arrival_date": "1720-04-14",
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


def make_scalar_result(items):
    mock = MagicMock()
    mock.scalars.return_value.all.return_value = items
    return mock


VOYAGE_1 = make_voyage(id=1, ship_name="Theeboom", year=1720, direction="outbound")
VOYAGE_2 = make_voyage(id=2, ship_name="Wind", year=1725, direction="inbound",
                       origin_name_raw="Batavia", destination_name_raw="Padang")


# ── Status & Content-Type ─────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_export_csv_returns_200_with_csv_content_type():
    """GET /api/voyages/export harus return 200 dengan Content-Type text/csv."""
    async def mock_get_db():
        session = AsyncMock()
        session.execute.return_value = make_scalar_result([VOYAGE_1])
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/voyages/export")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert "text/csv" in response.headers.get("content-type", "")


@pytest.mark.asyncio
async def test_export_csv_has_content_disposition_attachment():
    """Response harus punya Content-Disposition: attachment agar browser memulai download."""
    async def mock_get_db():
        session = AsyncMock()
        session.execute.return_value = make_scalar_result([VOYAGE_1])
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/voyages/export")

    app.dependency_overrides.clear()

    cd = response.headers.get("content-disposition", "")
    assert "attachment" in cd, f"Content-Disposition harus 'attachment', dapat: {cd!r}"
    assert ".csv" in cd, f"Filename harus berakhir .csv, dapat: {cd!r}"


# ── CSV structure ─────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_export_csv_contains_header_row():
    """Baris pertama CSV harus berisi nama kolom yang benar."""
    async def mock_get_db():
        session = AsyncMock()
        session.execute.return_value = make_scalar_result([VOYAGE_1])
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/voyages/export")

    app.dependency_overrides.clear()

    lines = response.text.strip().splitlines()
    assert lines, "Response CSV kosong"
    header_line = lines[0]
    for col in CSV_HEADERS:
        assert col in header_line, (
            f"Kolom '{col}' tidak ada di header CSV.\nHeader: {header_line}"
        )


@pytest.mark.asyncio
async def test_export_csv_contains_voyage_data():
    """Baris ke-2 CSV harus berisi data voyage (ship_name, year, direction)."""
    async def mock_get_db():
        session = AsyncMock()
        session.execute.return_value = make_scalar_result([VOYAGE_1])
        yield session

    from database import get_db
    app.dependency_overrides[get_db] = mock_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/voyages/export")

    app.dependency_overrides.clear()

    lines = response.text.strip().splitlines()
    assert len(lines) >= 2, f"CSV harus punya ≥2 baris (header + data), dapat {len(lines)}"
    data_line = lines[1]
    assert "Theeboom" in data_line, f"ship_name 'Theeboom' tidak ada di baris data: {data_line}"
    assert "1720" in data_line, f"year '1720' tidak ada di baris data: {data_line}"
    assert "outbound" in data_line, f"direction 'outbound' tidak ada di baris data: {data_line}"
