"""add_amh_images_to_forts

Revision ID: 002_amh_images
Revises: 001
Create Date: 2026-06-28

Sprint ATM Westkust Routes — US-06 (extended)
Menambahkan kolom amh_images (JSONB) ke tabel forts untuk menyimpan
daftar gambar dari Atlas of Mutual Heritage (AMH) per fort.

Kolom nullable agar migration aman di data existing.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "002_amh_images"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "forts",
        sa.Column("amh_images", postgresql.JSONB, nullable=True),
    )


def downgrade() -> None:
    op.drop_column("forts", "amh_images")
