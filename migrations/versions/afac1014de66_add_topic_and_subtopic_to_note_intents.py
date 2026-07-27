"""add topic and subtopic to note_intents

Revision ID: afac1014de66
Revises: 4f1b82a7c930
Create Date: 2026-07-10 16:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "afac1014de66"
down_revision: Union[str, Sequence[str], None] = "4f1b82a7c930"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "note_intents",
        sa.Column("topic", sa.String(length=120), nullable=True),
    )
    op.add_column(
        "note_intents",
        sa.Column("subtopic", sa.String(length=120), nullable=True),
    )
    # Drop the old unique constraint on note_id (one intent per note)
    # and replace with a non-unique index to allow future multi-intent support
    op.drop_constraint("note_intents_note_id_key", "note_intents", type_="unique")
    op.create_index(
        "ix_note_intents_note_id_unique",
        "note_intents",
        ["note_id"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index("ix_note_intents_note_id_unique", table_name="note_intents")
    op.create_unique_constraint("note_intents_note_id_key", "note_intents", ["note_id"])
    op.drop_column("note_intents", "subtopic")
    op.drop_column("note_intents", "topic")
