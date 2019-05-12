"""empty message

Revision ID: 2057ec8a1b29
Revises: e3dac9fc51a5
Create Date: 2019-05-11 17:50:23.118234

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2057ec8a1b29'
down_revision = 'e3dac9fc51a5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('modified_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('email_address', sa.String(length=120), nullable=True),
    sa.Column('first_name', sa.String(length=64), nullable=False),
    sa.Column('last_name', sa.String(length=64), nullable=True),
    sa.Column('joined', sa.Date(), server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email_address'), 'users', ['email_address'], unique=True)
    op.create_index(op.f('ix_users_first_name'), 'users', ['first_name'], unique=False)
    op.create_index(op.f('ix_users_joined'), 'users', ['joined'], unique=False)
    op.create_index(op.f('ix_users_last_name'), 'users', ['last_name'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.drop_index('ix_user_email_address', table_name='user')
    op.drop_index('ix_user_first_name', table_name='user')
    op.drop_index('ix_user_joined', table_name='user')
    op.drop_index('ix_user_last_name', table_name='user')
    op.drop_index('ix_user_username', table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('modified_at', postgresql.TIMESTAMP(), server_default=sa.text("timezone('utc'::text, now())"), autoincrement=False, nullable=False),
    sa.Column('username', sa.VARCHAR(length=64), autoincrement=False, nullable=False),
    sa.Column('email_address', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.Column('first_name', sa.VARCHAR(length=64), autoincrement=False, nullable=False),
    sa.Column('last_name', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.Column('joined', sa.DATE(), server_default=sa.text("timezone('utc'::text, now())"), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='user_pkey')
    )
    op.create_index('ix_user_username', 'user', ['username'], unique=True)
    op.create_index('ix_user_last_name', 'user', ['last_name'], unique=False)
    op.create_index('ix_user_joined', 'user', ['joined'], unique=False)
    op.create_index('ix_user_first_name', 'user', ['first_name'], unique=False)
    op.create_index('ix_user_email_address', 'user', ['email_address'], unique=True)
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_last_name'), table_name='users')
    op.drop_index(op.f('ix_users_joined'), table_name='users')
    op.drop_index(op.f('ix_users_first_name'), table_name='users')
    op.drop_index(op.f('ix_users_email_address'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
