"""add extraction_quality_score to note_intents

Revision ID: d4e5f6a7b8c9
Revises: b1c2d3e4f5a6
Create Date: 2026-07-27 00:00:00.000000

WHY: Stores a [0.0, 1.0] per-extraction quality score so that low-quality
extractions can be identified for re-processing and deprioritised in
retrieval. Column is nullable so existing rows receive NULL on upgrade and
can be populated by scripts/backfill_quality_score.py without downtime.

No index is added at this time — there is currently no query that filters
on this column. Add an index when a query that benefits from it is
implemented.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "d4e5f6a7b8c9"
down_revision: Union[str, Sequence[str], None] = "b1c2d3e4f5a6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "note_intents",
        sa.Column(
            "extraction_quality_score",
            sa.Float(),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column("note_intents", "extraction_quality_score")
