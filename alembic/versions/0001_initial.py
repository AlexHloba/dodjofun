"""create initial tables

Revision ID: 0001_initial
Revises: 
Create Date: 2025-10-20 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(), nullable=False, unique=True, index=True),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('level', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('xp', sa.Integer(), nullable=False, server_default='0'),
    )

    op.create_table(
        'lessons',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('video_url', sa.String(), nullable=True),
        sa.Column('xp_reward', sa.Integer(), nullable=False, server_default='50'),
        sa.Column('prerequisite', sa.Integer(), sa.ForeignKey('lessons.id'), nullable=True),
    )

    op.create_table(
        'progress',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id')),
        sa.Column('lesson_id', sa.Integer(), sa.ForeignKey('lessons.id')),
        sa.Column('completed', sa.Boolean(), nullable=False, server_default='false'),
    )


def downgrade():
    op.drop_table('progress')
    op.drop_table('lessons')
    op.drop_table('users')
