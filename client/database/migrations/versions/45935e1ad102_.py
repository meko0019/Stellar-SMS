"""empty message

Revision ID: 45935e1ad102
Revises: 
Create Date: 2019-06-04 10:40:08.192236

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "45935e1ad102"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "modified_at",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.Column("username", sa.String(length=64), nullable=False),
        sa.Column("email_address", sa.String(length=120), nullable=True),
        sa.Column("phone_number", sa.String(length=32), nullable=True),
        sa.Column("first_name", sa.String(length=64), nullable=False),
        sa.Column("last_name", sa.String(length=64), nullable=True),
        sa.Column(
            "joined",
            sa.Date(),
            server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
            nullable=True,
        ),
        sa.Column("password_hash", sa.String(length=128), nullable=True),
        sa.Column(
            "password_required", sa.Boolean(), server_default="false", nullable=True
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_users_email_address"), "users", ["email_address"], unique=True
    )
    op.create_index(op.f("ix_users_first_name"), "users", ["first_name"], unique=False)
    op.create_index(op.f("ix_users_joined"), "users", ["joined"], unique=False)
    op.create_index(op.f("ix_users_last_name"), "users", ["last_name"], unique=False)
    op.create_index(
        op.f("ix_users_phone_number"), "users", ["phone_number"], unique=True
    )
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=True)
    op.create_table(
        "messages",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "modified_at",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.Column("msg_id", sa.String(length=64), nullable=False),
        sa.Column("body", sa.String(length=128), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("unread", sa.Boolean(), server_default="true", nullable=True),
        sa.Column(
            "time_created",
            sa.Date(),
            server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
            nullable=True,
        ),
        sa.Column("recieved_at", sa.Date(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_messages_body"), "messages", ["body"], unique=False)
    op.create_index(op.f("ix_messages_msg_id"), "messages", ["msg_id"], unique=True)
    op.create_index(
        op.f("ix_messages_recieved_at"), "messages", ["recieved_at"], unique=False
    )
    op.create_index(
        op.f("ix_messages_time_created"), "messages", ["time_created"], unique=False
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_messages_time_created"), table_name="messages")
    op.drop_index(op.f("ix_messages_recieved_at"), table_name="messages")
    op.drop_index(op.f("ix_messages_msg_id"), table_name="messages")
    op.drop_index(op.f("ix_messages_body"), table_name="messages")
    op.drop_table("messages")
    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.drop_index(op.f("ix_users_phone_number"), table_name="users")
    op.drop_index(op.f("ix_users_last_name"), table_name="users")
    op.drop_index(op.f("ix_users_joined"), table_name="users")
    op.drop_index(op.f("ix_users_first_name"), table_name="users")
    op.drop_index(op.f("ix_users_email_address"), table_name="users")
    op.drop_table("users")
    # ### end Alembic commands ###