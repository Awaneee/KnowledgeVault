"""add avatar_path to users

Revision ID: a4b5c6d7e8f9
Revises: f9a1b2c3d4e5
Create Date: 2026-09-05
"""
from typing import Union, Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "a4b5c6d7e8f9"
down_revision: Union[str, Sequence[str], None] = "f9a1b2c3d4e5"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("avatar_path", sa.String(255), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("users", "avatar_path")
