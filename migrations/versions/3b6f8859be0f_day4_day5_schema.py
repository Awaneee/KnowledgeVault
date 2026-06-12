"""day4_day5_schema

Revision ID: 3b6f8859be0f
Revises: 11e5884eca2c
Create Date: 2026-06-12 22:48:34.547917
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3b6f8859be0f"
down_revision: Union[str, Sequence[str], None] = "11e5884eca2c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # ==========================================================
    # Evaluation Dataset
    # ==========================================================

    op.create_table(
        "evaluation_datasets",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("note_text", sa.Text(), nullable=False),
        sa.Column("expected_category", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # ==========================================================
    # Classification Feedback
    # ==========================================================

    op.create_table(
        "classification_feedback",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("note_id", sa.Integer(), nullable=False),
        sa.Column("predicted_category_id", sa.Integer(), nullable=False),
        sa.Column("corrected_category_id", sa.Integer(), nullable=False),
        sa.Column("confidence_score", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["note_id"],
            ["notes.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["predicted_category_id"],
            ["categories.id"],
        ),
        sa.ForeignKeyConstraint(
            ["corrected_category_id"],
            ["categories.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # ==========================================================
    # Embeddings (RAW SQL + PGVECTOR)
    # ==========================================================

    op.execute(
        """
        CREATE TABLE embeddings (
            id SERIAL PRIMARY KEY,
            note_id INTEGER NOT NULL UNIQUE,
            embedding_model VARCHAR(100) NOT NULL,
            embedding_vector VECTOR(384) NOT NULL,
            created_at TIMESTAMP NOT NULL,
            CONSTRAINT fk_embedding_note
                FOREIGN KEY (note_id)
                REFERENCES notes(id)
                ON DELETE CASCADE
        )
        """
    )

    # ==========================================================
    # Categories
    # ==========================================================

    op.add_column(
        "categories",
        sa.Column(
            "description",
            sa.String(length=500),
            nullable=True,
        ),
    )

    op.add_column(
        "categories",
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
    )

    # ==========================================================
    # Notes
    # ==========================================================

    op.add_column(
        "notes",
        sa.Column(
            "source_type",
            sa.String(),
            server_default="manual_note",
            nullable=False,
        ),
    )

    op.add_column(
        "notes",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("notes", "updated_at")
    op.drop_column("notes", "source_type")

    op.drop_column("categories", "updated_at")
    op.drop_column("categories", "description")

    op.drop_table("classification_feedback")
    op.drop_table("evaluation_datasets")

    op.execute("DROP TABLE IF EXISTS embeddings")