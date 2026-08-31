"""add password reset fields to users

Revision ID: f9a1b2c3d4e5
Revises: e7f8a9b0c1d2
Create Date: 2026-08-31
"""
from typing import Union, Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "f9a1b2c3d4e5"
down_revision: Union[str, Sequence[str], None] = "e7f8a9b0c1d2"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("reset_token_hash", sa.String(128), nullable=True),
    )
    op.add_column(
        "users",
        sa.Column("reset_token_expires_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_users_reset_token_hash", "users", ["reset_token_hash"])


def downgrade() -> None:
    op.drop_index("ix_users_reset_token_hash", table_name="users")
    op.drop_column("users", "reset_token_expires_at")
    op.drop_column("users", "reset_token_hash")
