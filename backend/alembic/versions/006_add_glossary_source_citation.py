"""add source_citation to commodity_glossary

Revision ID: 006
Revises: 005
Create Date: 2026-07-07

Technical debt dari docs/prd/prd-port-tally-aggregate.md: commodity_glossary tidak
punya cara melacak "definisi ini dari mana". NULL utk 201 entri existing (asal
tak tercatat) -- BUKAN ditebak. Entri satuan baru (pikol/kati/bahar/last/taël/pon)
diisi eksplisit rujuk VOC-Glossarium.
"""
from alembic import op
import sqlalchemy as sa

revision = '006'
down_revision = '005'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('commodity_glossary', sa.Column('source_citation', sa.Text(), nullable=True))


def downgrade():
    op.drop_column('commodity_glossary', 'source_citation')
