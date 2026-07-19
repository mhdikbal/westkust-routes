"""add port_arrival_tallies table

Revision ID: 005
Revises: 004
Create Date: 2026-07-07

docs/prd/prd-port-tally-aggregate.md -- rekap kedatangan bulanan multi-kapal-tak-bernama
dari Dagh-register (record_type=port_tally_aggregate), tidak cocok skema Voyage
(ship_name nullable=False). Satu staging_extraction -> banyak baris di sini
(satu per kelompok-pelabuhan-asal per bulan).
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

revision = '005'
down_revision = '004'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'port_arrival_tallies',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('staging_extraction_id', sa.Integer(), sa.ForeignKey('staging_extractions.id'), nullable=False),
        sa.Column('volume', sa.String(100), nullable=False),
        sa.Column('tanggal_perkiraan', sa.String(50), nullable=True),
        sa.Column('origin_port_raw', sa.String(100), nullable=False),
        sa.Column('origin_fort_id', sa.Integer(), sa.ForeignKey('forts.id'), nullable=True),
        sa.Column('ship_count', sa.Integer(), nullable=True),
        sa.Column('person_count', sa.Integer(), nullable=True),
        sa.Column('cargo_text', sa.Text(), nullable=False),
        sa.Column('cargo_items_json', JSONB, nullable=True),
        sa.Column('confidence_flag', sa.String(20), nullable=False, server_default='unverified'),
        sa.Column('created_at', sa.String(30), nullable=False),
    )
    op.create_index('ix_port_arrival_tallies_staging_extraction_id', 'port_arrival_tallies', ['staging_extraction_id'])
    op.create_index('ix_port_arrival_tallies_origin_fort_id', 'port_arrival_tallies', ['origin_fort_id'])


def downgrade():
    op.drop_index('ix_port_arrival_tallies_origin_fort_id', table_name='port_arrival_tallies')
    op.drop_index('ix_port_arrival_tallies_staging_extraction_id', table_name='port_arrival_tallies')
    op.drop_table('port_arrival_tallies')
