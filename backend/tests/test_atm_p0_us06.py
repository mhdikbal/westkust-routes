"""
US-06: Schema Migration — Fort AMH Enrichment Columns

TDD RED phase: test ini harus FAIL sebelum migration dijalankan,
karena kolom nama_historis, designasi_voc, fungsi_historis,
periode_aktif, amh_url belum ada di tabel forts.

Setelah alembic upgrade head → semua test di sini harus PASS (GREEN).
"""
import pytest
import os
import sys
from sqlalchemy import create_engine, inspect, text

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SYNC_DB_URL = os.getenv(
    "SYNC_DATABASE_URL",
    "postgresql://vocuser:***REDACTED***@voc_db:5432/vocdb"
)

NEW_COLUMNS = {
    "nama_historis":   "character varying",
    "designasi_voc":   "character varying",
    "fungsi_historis": "text",
    "periode_aktif":   "int4range",
    "amh_url":         "character varying",
}

NEW_INDEXES = [
    "idx_forts_periode_aktif",
    "idx_forts_designasi_voc",
    "idx_voyages_year",
    "idx_voyages_direction_year",
]


@pytest.fixture(scope="module")
def sync_engine():
    engine = create_engine(SYNC_DB_URL)
    yield engine
    engine.dispose()


def test_fort_new_columns_exist(sync_engine):
    """Semua 5 kolom baru harus ada di tabel forts setelah migration."""
    inspector = inspect(sync_engine)
    columns = {c["name"]: c for c in inspector.get_columns("forts")}

    for col_name in NEW_COLUMNS:
        assert col_name in columns, (
            f"Kolom '{col_name}' belum ada di tabel forts. "
            f"Jalankan: docker compose exec backend alembic upgrade head"
        )


def test_fort_new_columns_are_nullable(sync_engine):
    """Semua kolom baru harus nullable (safe migration, tidak rusak data existing)."""
    inspector = inspect(sync_engine)
    columns = {c["name"]: c for c in inspector.get_columns("forts")}

    for col_name in NEW_COLUMNS:
        if col_name in columns:
            assert columns[col_name]["nullable"], (
                f"Kolom '{col_name}' harus nullable agar migration aman di data existing"
            )


def test_amh_url_check_constraint_exists(sync_engine):
    """Constraint chk_forts_amh_url_format harus ada untuk validasi domain AMH."""
    with sync_engine.connect() as conn:
        result = conn.execute(text("""
            SELECT COUNT(*) FROM information_schema.table_constraints
            WHERE table_name = 'forts'
            AND constraint_type = 'CHECK'
            AND constraint_name = 'chk_forts_amh_url_format'
        """))
        count = result.scalar()
    assert count == 1, (
        "Constraint chk_forts_amh_url_format tidak ditemukan di tabel forts"
    )


def test_new_indexes_exist(sync_engine):
    """Index baru untuk performance time-slider dan direction filter harus ada."""
    with sync_engine.connect() as conn:
        result = conn.execute(text("""
            SELECT indexname FROM pg_indexes
            WHERE tablename IN ('forts', 'voyages')
            AND indexname = ANY(:names)
        """), {"names": NEW_INDEXES})
        found = {row[0] for row in result.fetchall()}

    missing = set(NEW_INDEXES) - found
    assert not missing, f"Index berikut belum dibuat: {missing}"


def test_existing_forts_data_intact(sync_engine):
    """Data fort existing tidak boleh berubah setelah migration."""
    with sync_engine.connect() as conn:
        count = conn.execute(text("SELECT COUNT(*) FROM forts")).scalar()
    assert count > 0, "Tabel forts kosong setelah migration — data hilang!"


def test_existing_voyages_data_intact(sync_engine):
    """Data voyage existing tidak boleh berubah setelah migration."""
    with sync_engine.connect() as conn:
        count = conn.execute(text("SELECT COUNT(*) FROM voyages")).scalar()
    # rev.11 (2026-07-08): pelabuhan pantai timur (Jambi/Palembang/Lampung) dihapus dari
    # skope atlas Westkust — 545 voyage timur ikut terhapus; baseline baru 4193 BGB + Dagh-register.
    assert count >= 4300, (
        f"Jumlah voyage berkurang di luar penghapusan pelabuhan timur rev.11: {count} (expected >= 4300)"
    )


def test_amh_url_constraint_rejects_invalid_url(sync_engine):
    """Constraint harus menolak URL yang bukan domain AMH atau Huygens."""
    with sync_engine.connect() as conn:
        try:
            conn.execute(text("""
                UPDATE forts SET amh_url = 'https://evil.com/hack'
                WHERE id = (SELECT MIN(id) FROM forts)
            """))
            conn.rollback()
            pytest.fail("Constraint tidak memblokir URL invalid — security issue!")
        except Exception as e:
            conn.rollback()
            assert "chk_forts_amh_url_format" in str(e).lower() or "check" in str(e).lower(), (
                f"Error bukan dari constraint: {e}"
            )


def test_amh_url_constraint_accepts_valid_amh_url(sync_engine):
    """Constraint harus menerima URL AMH yang valid."""
    with sync_engine.connect() as conn:
        try:
            conn.execute(text("""
                UPDATE forts
                SET amh_url = 'https://www.atlasofmutualheritage.nl/page/5751/padang'
                WHERE id = (SELECT MIN(id) FROM forts)
            """))
            conn.rollback()
        except Exception as e:
            conn.rollback()
            pytest.fail(f"URL AMH valid ditolak oleh constraint: {e}")
