"""add source_document to atjeh_trade_records

Revision ID: 008
Revises: 007
Create Date: 2026-07-13

Kedua volume Dagh-register Batavia (1643-1644 dan 1631-1634) sekarang jadi
sumber tabel ini -- source_page saja ambigu lintas volume (mis. hal. 164
berisi konten berbeda di tiap volume). Backfill 25 baris existing sbg
'1643-1644' (satu-satunya volume tersisir saat baris itu dibuat), lalu
kunci NOT NULL supaya baris baru wajib menyatakan asalnya.
"""
from alembic import op
import sqlalchemy as sa

revision = '008'
down_revision = '007'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('atjeh_trade_records', sa.Column('source_document', sa.String(20), nullable=True))
    op.execute("UPDATE atjeh_trade_records SET source_document = '1643-1644' WHERE source_document IS NULL")
    op.alter_column('atjeh_trade_records', 'source_document', nullable=False)


def downgrade():
    op.drop_column('atjeh_trade_records', 'source_document')
