"""add conversation_sessions and conversation_messages tables

Revision ID: a1b2c3d4e5f6
Revises: c8d9e0f1a2b3
Create Date: 2026-08-25 00:00:00.000000

WHY: Adds persistent multi-turn conversation history so users can ask
follow-up questions with full context of previous turns.  Each session
belongs to one user and contains an ordered list of messages (user /
assistant roles).  The assistant messages store citation metadata as JSON
so clients can render source links without an extra round-trip.
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, Sequence[str], None] = "c8d9e0f1a2b3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "conversation_sessions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_conversation_sessions_id"), "conversation_sessions", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_conversation_sessions_user_id"),
        "conversation_sessions",
        ["user_id"],
        unique=False,
    )

    op.create_table(
        "conversation_messages",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("session_id", sa.Integer(), nullable=False),
        sa.Column("role", sa.String(length=20), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("citations", sa.JSON(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["session_id"], ["conversation_sessions.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_conversation_messages_id"), "conversation_messages", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_conversation_messages_session_id"),
        "conversation_messages",
        ["session_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_conversation_messages_session_id"), table_name="conversation_messages"
    )
    op.drop_index(
        op.f("ix_conversation_messages_id"), table_name="conversation_messages"
    )
    op.drop_table("conversation_messages")
    op.drop_index(
        op.f("ix_conversation_sessions_user_id"), table_name="conversation_sessions"
    )
    op.drop_index(
        op.f("ix_conversation_sessions_id"), table_name="conversation_sessions"
    )
    op.drop_table("conversation_sessions")
