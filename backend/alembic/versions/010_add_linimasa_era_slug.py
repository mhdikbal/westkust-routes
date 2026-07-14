"""add era_slug to linimasa_events

Revision ID: 010
Revises: 009
Create Date: 2026-07-14

Fase 1 "/linimasa" (docs/prd-linimasa-kronik-pantai-barat.md): kelompokkan 30
event yang sudah ada jadi 5 babak naratif (era_slug) berbasis rentang tahun yg
benar-benar punya event bersitasi (1625-1681) -- bukan skema 1600-1690 penuh
dari design spec sumber. Label/headline per era disimpan di frontend
(map_app/views.py ERAS dict), bukan kolom baru di sini.
"""
from alembic import op
import sqlalchemy as sa

revision = '010'
down_revision = '009'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('linimasa_events', sa.Column('era_slug', sa.String(40), nullable=True))
    op.create_index('ix_linimasa_events_era_slug', 'linimasa_events', ['era_slug'])


def downgrade():
    op.drop_index('ix_linimasa_events_era_slug', table_name='linimasa_events')
    op.drop_column('linimasa_events', 'era_slug')
