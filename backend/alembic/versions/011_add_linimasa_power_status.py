"""add fort_id/dominion_status/tags to linimasa_events

Revision ID: 011
Revises: 010
Create Date: 2026-07-17

Model 2 rantai Markov `dominion_status` (docs/prd/prd-atlas-power-model.md,
docs/prd/prd-pemodelan-kekuasaan-dagang.md §6 blocker) -- 3 kolom nullable + index
di fort_id dan dominion_status, ikuti pola persis 010_add_linimasa_era_slug.py.
Backfill data (CSV + seed_linimasa_events.py validasi) dikerjakan terpisah,
BERTAHAP per PRD §6, bukan bagian migrasi ini.
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '011'
down_revision = '010'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('linimasa_events', sa.Column('fort_id', sa.Integer(), sa.ForeignKey('forts.id'), nullable=True))
    op.add_column('linimasa_events', sa.Column('dominion_status', sa.String(30), nullable=True))
    op.add_column('linimasa_events', sa.Column('tags', postgresql.ARRAY(sa.Text()), nullable=True))
    op.create_index('ix_linimasa_events_fort_id', 'linimasa_events', ['fort_id'])
    op.create_index('ix_linimasa_events_dominion_status', 'linimasa_events', ['dominion_status'])


def downgrade():
    op.drop_index('ix_linimasa_events_dominion_status', table_name='linimasa_events')
    op.drop_index('ix_linimasa_events_fort_id', table_name='linimasa_events')
    op.drop_column('linimasa_events', 'tags')
    op.drop_column('linimasa_events', 'dominion_status')
    op.drop_column('linimasa_events', 'fort_id')
