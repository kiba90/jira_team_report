"""new_worklog

Revision ID: 27d7bc410b70
Revises: f26fd897137f
Create Date: 2021-02-08 15:32:40.695674

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '27d7bc410b70'
down_revision = 'f26fd897137f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('jira_work_stat', sa.Column('not_completed_worklog', sa.INTEGER(), nullable=True))
    op.drop_column('jira_work_stat', 'total_worklog')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('jira_work_stat', sa.Column('total_worklog', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('jira_work_stat', 'not_completed_worklog')
    # ### end Alembic commands ###
