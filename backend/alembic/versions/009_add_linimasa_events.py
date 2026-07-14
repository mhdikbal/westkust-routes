"""add linimasa_events table

Revision ID: 009
Revises: 008
Create Date: 2026-07-14

Tabel baru utk halaman /linimasa -- peristiwa suksesi/politik kekuasaan Atjeh
atas pantai barat Sumatra, dari Sultan Iskandar Muda sampai Traktat Painan
1663. Terpisah dari atjeh_trade_records (yang scope-nya "dagang dari/ke/di
Atjeh") -- lihat docstring LinimasaEvent di models.py.
"""
from alembic import op
import sqlalchemy as sa

revision = '009'
down_revision = '008'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'linimasa_events',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('source_document', sa.String(20), nullable=False),
        sa.Column('source_page', sa.Integer(), nullable=False),
        sa.Column('book_page', sa.String(20), nullable=True),
        sa.Column('event_date_raw', sa.String(50), nullable=True),
        sa.Column('year', sa.Integer(), nullable=True),
        sa.Column('event_type', sa.String(20), nullable=False),
        sa.Column('ruler_actor', sa.String(200), nullable=True),
        sa.Column('title', sa.String(300), nullable=False),
        sa.Column('text_asli', sa.Text(), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('confidence_flag', sa.String(20), nullable=False, server_default='unverified'),
        sa.Column('created_at', sa.String(30), nullable=False),
    )
    op.create_index('ix_linimasa_events_source_document', 'linimasa_events', ['source_document'])
    op.create_index('ix_linimasa_events_source_page', 'linimasa_events', ['source_page'])
    op.create_index('ix_linimasa_events_year', 'linimasa_events', ['year'])
    op.create_index('ix_linimasa_events_event_type', 'linimasa_events', ['event_type'])


def downgrade():
    op.drop_index('ix_linimasa_events_event_type', table_name='linimasa_events')
    op.drop_index('ix_linimasa_events_year', table_name='linimasa_events')
    op.drop_index('ix_linimasa_events_source_page', table_name='linimasa_events')
    op.drop_index('ix_linimasa_events_source_document', table_name='linimasa_events')
    op.drop_table('linimasa_events')
