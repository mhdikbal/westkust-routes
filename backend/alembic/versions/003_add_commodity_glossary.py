"""add commodity_glossary table

Revision ID: 003
Revises: 002
Create Date: 2026-06-29
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY, TEXT

revision = '003'
# Menunjuk revision-id aktual file 002 ("002_amh_images"), bukan prefiks nama
# file — chain sempat putus (KeyError '002') dan memblokir semua migration.
down_revision = '002_amh_images'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'commodity_glossary',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('term', sa.String(200), nullable=False, unique=True),
        sa.Column('term_display', sa.String(200), nullable=True),
        sa.Column('variants', ARRAY(TEXT), nullable=True, server_default='{}'),
        sa.Column('definition_nl', sa.Text(), nullable=True),
        sa.Column('definition_id', sa.Text(), nullable=True),  # terjemahan Indonesia
        sa.Column('category', sa.String(100), nullable=True),  # rempah, logam, tekstil, dsb
    )
    # Index untuk lookup cepat dari frontend/API
    op.create_index('ix_glossary_term', 'commodity_glossary', ['term'])
    # GIN index untuk pencarian ke dalam array variants
    op.execute(
        "CREATE INDEX ix_glossary_variants ON commodity_glossary USING GIN (variants)"
    )


def downgrade():
    op.drop_index('ix_glossary_variants', table_name='commodity_glossary')
    op.drop_index('ix_glossary_term', table_name='commodity_glossary')
    op.drop_table('commodity_glossary')
