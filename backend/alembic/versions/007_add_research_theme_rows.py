"""add research_theme_rows table

Revision ID: 007
Revises: 006
Create Date: 2026-07-08

docs/prd/prd-sankey-tema-korpus.md + docs/sprint/sprint-sankey-tema-korpus.md (SNK-1) --
hasil klasifikasi zero-shot tema-korpus (GLOBALISE + Dagh-register, 1.005 baris),
sumber Sankey tema-korpus namespace `research`. Idempotent by corpus_id.
"""
from alembic import op
import sqlalchemy as sa

revision = '007'
down_revision = '006'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'research_theme_rows',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('corpus_id', sa.Integer(), nullable=False),
        sa.Column('corpus_asal', sa.String(20), nullable=False),
        sa.Column('source', sa.String(50), nullable=True),
        sa.Column('volume', sa.String(200), nullable=True),
        sa.Column('inventaris_ref', sa.String(100), nullable=True),
        sa.Column('tanggal_perkiraan', sa.Text(), nullable=True),
        sa.Column('tahun', sa.Integer(), nullable=True),
        sa.Column('dekade', sa.Integer(), nullable=True),
        sa.Column('pelabuhan_disebut', sa.String(300), nullable=False),
        sa.Column('tema_dominan', sa.String(30), nullable=False),
        sa.Column('skor_dominan', sa.Float(), nullable=True),
        sa.Column('low_confidence', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('skor_pdr_drainase', sa.Float(), nullable=True),
        sa.Column('skor_etr_retensi', sa.Float(), nullable=True),
        sa.Column('skor_hak_adat', sa.Float(), nullable=True),
        sa.Column('skor_pelayaran', sa.Float(), nullable=True),
        sa.Column('skor_sengketa', sa.Float(), nullable=True),
        sa.Column('skor_syahbandar', sa.Float(), nullable=True),
        sa.Column('skor_tidak_relevan', sa.Float(), nullable=True),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('text_asli', sa.Text(), nullable=True),
    )
    op.create_index('ix_research_theme_rows_corpus_id', 'research_theme_rows', ['corpus_id'], unique=True)
    op.create_index('ix_research_theme_rows_corpus_asal', 'research_theme_rows', ['corpus_asal'])
    op.create_index('ix_research_theme_rows_tahun', 'research_theme_rows', ['tahun'])
    op.create_index('ix_research_theme_rows_dekade', 'research_theme_rows', ['dekade'])
    op.create_index('ix_research_theme_rows_tema_dominan', 'research_theme_rows', ['tema_dominan'])
    op.create_index('ix_research_theme_rows_low_confidence', 'research_theme_rows', ['low_confidence'])
    op.create_index('ix_research_theme_dekade_tema', 'research_theme_rows', ['dekade', 'tema_dominan'])


def downgrade():
    op.drop_index('ix_research_theme_dekade_tema', table_name='research_theme_rows')
    op.drop_index('ix_research_theme_rows_low_confidence', table_name='research_theme_rows')
    op.drop_index('ix_research_theme_rows_tema_dominan', table_name='research_theme_rows')
    op.drop_index('ix_research_theme_rows_dekade', table_name='research_theme_rows')
    op.drop_index('ix_research_theme_rows_tahun', table_name='research_theme_rows')
    op.drop_index('ix_research_theme_rows_corpus_asal', table_name='research_theme_rows')
    op.drop_index('ix_research_theme_rows_corpus_id', table_name='research_theme_rows')
    op.drop_table('research_theme_rows')
