"""velocity_stats

Revision ID: 50c669c31ca0
Revises: 
Create Date: 2021-01-14 22:21:46.960700

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50c669c31ca0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('jira-velocity',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('project_key', sa.VARCHAR(length=256), nullable=False),
    sa.Column('sprint_id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=256), nullable=False),
    sa.Column('commitment', sa.FLOAT(), nullable=False),
    sa.Column('completed', sa.FLOAT(), nullable=False),
    sa.Column('start_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('end_at', sa.TIMESTAMP(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('sprint_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('jira-velocity')
    # ### end Alembic commands ###
