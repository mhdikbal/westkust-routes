"""add fort_model_metrics table

Revision ID: 012
Revises: 011
Create Date: 2026-07-24

Ringkasan output Model 2/5/6 (Markov/System Dynamics/Game Theory) per fort --
snapshot terbaru (bukan histori), dipakai layer /atlas (pennant klaster,
cincin kestabilan, sparkline). Lihat memory project_padang_hinterland_gaps
arahan MLOPS+DBA, docs/thesis/colab/model5_system_dynamics_1d.py.
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '012'
down_revision = '011'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'fort_model_metrics',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('fort_id', sa.Integer(), sa.ForeignKey('forts.id'), nullable=False, unique=True),
        sa.Column('cluster', sa.String(20), nullable=False),
        sa.Column('p_self_current_status', sa.Float(), nullable=True),
        sa.Column('dynamics_series', postgresql.JSONB(), nullable=True),
        sa.Column('rmse', sa.Float(), nullable=True),
        sa.Column('computed_at', sa.String(30), nullable=False),
    )
    op.create_index('ix_fort_model_metrics_fort_id', 'fort_model_metrics', ['fort_id'])


def downgrade():
    op.drop_index('ix_fort_model_metrics_fort_id', table_name='fort_model_metrics')
    op.drop_table('fort_model_metrics')
