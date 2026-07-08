"""add source (provenance) column to voyages

Revision ID: 004
Revises: 003
Create Date: 2026-07-07

P0.3b (docs/prd-cleaning-daghregister-1660-1669.md) -- Voyage sebelumnya tidak
punya kolom yang menandai provenance (source_url cuma link eksternal, bukan
label). Kolom baru ini membedakan data BGB Huygens (default, existing) dari
hasil promosi staging Dagh-register/GLOBALISE, dipakai frontend utk toggle +
label sumber di modal voyage.
"""
from alembic import op
import sqlalchemy as sa

revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'voyages',
        sa.Column('source', sa.String(50), nullable=False, server_default='bgb_huygens'),
    )
    op.create_index('ix_voyages_source', 'voyages', ['source'])


def downgrade():
    op.drop_index('ix_voyages_source', table_name='voyages')
    op.drop_column('voyages', 'source')
