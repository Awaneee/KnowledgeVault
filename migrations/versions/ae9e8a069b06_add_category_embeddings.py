"""add category embeddings

Revision ID: ae9e8a069b06
Revises: 3b6f8859be0f
Create Date: 2026-06-15 00:30:46.499597
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector


# revision identifiers, used by Alembic.
revision: str = "ae9e8a069b06"
down_revision: Union[str, Sequence[str], None] = "3b6f8859be0f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "category_embeddings",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "category_id",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "embedding_model",
            sa.String(length=100),
            nullable=False
        ),
        sa.Column(
            "embedding_vector",
            Vector(384),
            nullable=False
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["categories.id"],
            ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("category_id")
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_table("category_embeddings")