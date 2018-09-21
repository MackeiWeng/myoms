"""empty message

Revision ID: d4522c50c5d6
Revises: 832d249ca957
Create Date: 2018-08-23 14:39:47.394500

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd4522c50c5d6'
down_revision = '832d249ca957'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'text')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('text', mysql.TEXT(), nullable=True))
    # ### end Alembic commands ###
