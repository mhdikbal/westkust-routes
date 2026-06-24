"""add_fort_historis_amh_fields

Revision ID: 001
Revises:
Create Date: 2026-06-24

Sprint ATM Westkust Routes — US-06
Menambahkan 5 kolom enrichment historis + AMH ke tabel forts:
  nama_historis, designasi_voc, fungsi_historis, periode_aktif, amh_url

Semua kolom nullable agar migration aman di data existing.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Aktifkan btree_gist untuk index GiST pada INT4RANGE
    op.execute("CREATE EXTENSION IF NOT EXISTS btree_gist")

    # Tambah 5 kolom enrichment ke tabel forts
    op.add_column("forts", sa.Column("nama_historis",   sa.String(255), nullable=True))
    op.add_column("forts", sa.Column("designasi_voc",   sa.String(100), nullable=True))
    op.add_column("forts", sa.Column("fungsi_historis", sa.Text(),      nullable=True))
    op.add_column("forts", sa.Column("periode_aktif",   postgresql.INT4RANGE(), nullable=True))
    op.add_column("forts", sa.Column("amh_url",         sa.String(500), nullable=True))

    # Constraint: amh_url hanya boleh domain AMH atau Huygens handle
    op.create_check_constraint(
        "chk_forts_amh_url_format",
        "forts",
        "amh_url IS NULL "
        "OR amh_url LIKE 'https://hdl.handle.net/%' "
        "OR amh_url LIKE 'https://www.atlasofmutualheritage.nl/%'",
    )

    # Index GiST untuk query range periode_aktif (time-slider P1-M2)
    op.create_index(
        "idx_forts_periode_aktif", "forts", ["periode_aktif"],
        postgresql_using="gist",
    )

    # Index partial untuk filter designasi_voc
    op.create_index(
        "idx_forts_designasi_voc", "forts", ["designasi_voc"],
        postgresql_where=sa.text("designasi_voc IS NOT NULL"),
    )

    # Index voyages.year untuk time-slider
    op.create_index("idx_voyages_year", "voyages", ["year"])

    # Composite index direction + year untuk filter kombinasi
    op.create_index(
        "idx_voyages_direction_year", "voyages", ["direction", "year"],
    )


def downgrade() -> None:
    op.drop_index("idx_voyages_direction_year", table_name="voyages")
    op.drop_index("idx_voyages_year",           table_name="voyages")
    op.drop_index("idx_forts_designasi_voc",    table_name="forts")
    op.drop_index("idx_forts_periode_aktif",    table_name="forts")
    op.drop_constraint("chk_forts_amh_url_format", "forts", type_="check")
    op.drop_column("forts", "amh_url")
    op.drop_column("forts", "periode_aktif")
    op.drop_column("forts", "fungsi_historis")
    op.drop_column("forts", "designasi_voc")
    op.drop_column("forts", "nama_historis")
