"""
Integration test (DB nyata, bukan mock) — regresi utk bug NULL-year exclusion
ditemukan 2026-07-07 saat promosi voyage Dagh-register: `Voyage.year >= year_from`
di SQL mengembalikan NULL (bukan false) kalau year IS NULL, jadi baris dgn year
tak diketahui SENYAP hilang dari SEMUA filter tahun -- sama persis kelas bug dgn
NULL-array guard di commodity_glossary (P0.5/glossary work, sesi yg sama).

8 dari 12 voyage Dagh-register yg baru dipromosikan punya year=NULL (jilid rentang
2 tahun spt "1666-1667", tak bisa dipastikan tahun tunggal tanpa menebak) --
sebelum fix, baris ini SELALU tersembunyi begitu user set year_from/year_to APA
PUN, termasuk default navbar (1660-1790) yg mestinya mencakupnya.
"""
import os
import sys
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import create_engine, text

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

SYNC_DB_URL = os.getenv("DATABASE_SYNC_URL", "postgresql://vocuser:***REDACTED***@db:5432/vocdb")


@pytest.fixture
def null_year_voyage():
    """Insert 1 voyage sementara dgn year=NULL, source unik utk isolasi; cleanup setelah test."""
    engine = create_engine(SYNC_DB_URL)
    marker = "test_null_year_voyage_regression"
    with engine.begin() as conn:
        conn.execute(text(
            "INSERT INTO voyages (ship_name, direction, source, source_url, year) "
            "VALUES ('Test Null Year Ship', 'outbound', 'daghregister_batavia', :marker, NULL)"
        ), {"marker": marker})
    yield marker
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM voyages WHERE source_url = :marker"), {"marker": marker})
    engine.dispose()


@pytest.mark.asyncio
async def test_list_voyages_year_filter_includes_null_year(null_year_voyage):
    """GET /api/voyages?year_from=1660&year_to=1790 harus TETAP menyertakan
    voyage dgn year=NULL (bukan disenyapkan oleh perbandingan SQL NULL)."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/voyages/?year_from=1660&year_to=1790&search=Test Null Year Ship")

    assert response.status_code == 200
    ships = [v["ship_name"] for v in response.json()]
    assert "Test Null Year Ship" in ships
