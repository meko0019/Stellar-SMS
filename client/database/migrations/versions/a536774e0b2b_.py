"""empty message

Revision ID: a536774e0b2b
Revises: cffecda0acbb
Create Date: 2019-06-06 11:04:37.824053

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a536774e0b2b'
down_revision = 'cffecda0acbb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('alias',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('modified_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('address', sa.String(length=128), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_alias_address'), 'alias', ['address'], unique=True)
    op.create_index(op.f('ix_alias_username'), 'alias', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_alias_username'), table_name='alias')
    op.drop_index(op.f('ix_alias_address'), table_name='alias')
    op.drop_table('alias')
    # ### end Alembic commands ###
