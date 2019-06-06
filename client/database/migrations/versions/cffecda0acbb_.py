"""empty message

Revision ID: cffecda0acbb
Revises: 70e1cf8d7a57
Create Date: 2019-06-06 10:41:47.728713

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cffecda0acbb'
down_revision = '70e1cf8d7a57'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('keypair_seed', sa.String(length=128), server_default='Null', nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'keypair_seed')
    # ### end Alembic commands ###
