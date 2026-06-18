"""add note auto organization metadata

Revision ID: 4f1b82a7c930
Revises: 8a3c2f1d9b7e
Create Date: 2026-06-18 03:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4f1b82a7c930"
down_revision: Union[str, Sequence[str], None] = "8a3c2f1d9b7e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "notes",
        sa.Column(
            "auto_title_source",
            sa.String(),
            server_default="legacy",
            nullable=False
        )
    )
    op.add_column(
        "notes",
        sa.Column(
            "organization_status",
            sa.String(),
            server_default="organized",
            nullable=False
        )
    )


def downgrade() -> None:
    op.drop_column("notes", "organization_status")
    op.drop_column("notes", "auto_title_source")
