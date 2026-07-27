"""add centroid_note_count to intent_category_embeddings

Revision ID: b1c2d3e4f5a6
Revises: afac1014de66
Create Date: 2026-07-26 00:00:00.000000

WHY: The previous embedding strategy overwrote the stored vector with a
re-encoding of the latest note's metadata on every assignment.  After N
assignments the vector represented only the last note, not the category.

The replacement is an incremental running mean (centroid):

    c_new = (c_old * N + v_new) / (N + 1)

centroid_note_count tracks how many note vectors have been folded into
the current centroid so the formula stays numerically correct across
restarts and re-runs.  The server_default of 1 is safe for existing rows:
they each hold a single-note encoding, so treating them as centroid_count=1
is accurate — the next assignment will blend correctly.
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b1c2d3e4f5a6"
down_revision: Union[str, Sequence[str], None] = "afac1014de66"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "intent_category_embeddings",
        sa.Column(
            "centroid_note_count",
            sa.Integer(),
            nullable=False,
            server_default="1",
        ),
    )


def downgrade() -> None:
    op.drop_column("intent_category_embeddings", "centroid_note_count")
