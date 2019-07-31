"""empty message

Revision ID: 9828fe4f68df
Revises: cfc92023cbaf
Create Date: 2019-07-31 12:51:32.441344

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9828fe4f68df'
down_revision = 'cfc92023cbaf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('payments', 'status')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('payments', sa.Column('status', sa.VARCHAR(length=16), autoincrement=False, nullable=True))
    # ### end Alembic commands ###