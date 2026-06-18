"""add intent organization

Revision ID: 8a3c2f1d9b7e
Revises: f583a18bd33a
Create Date: 2026-06-18 02:00:00.000000

"""
from typing import Sequence, Union

import pgvector

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "8a3c2f1d9b7e"
down_revision: Union[str, Sequence[str], None] = "f583a18bd33a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "intent_categories",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("description", sa.String(length=500), nullable=True),
        sa.Column("intent_type", sa.String(length=50), nullable=False),
        sa.Column("actor", sa.String(length=120), nullable=True),
        sa.Column("action", sa.String(length=80), nullable=True),
        sa.Column("time_scope", sa.String(length=50), nullable=True),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("source", sa.String(length=50), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("note_count", sa.Integer(), nullable=False),
        sa.Column("last_used_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_intent_categories_actor"), "intent_categories", ["actor"], unique=False)
    op.create_index(op.f("ix_intent_categories_intent_type"), "intent_categories", ["intent_type"], unique=False)
    op.create_index(op.f("ix_intent_categories_user_id"), "intent_categories", ["user_id"], unique=False)

    op.create_table(
        "note_intents",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("note_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("intent_type", sa.String(length=50), nullable=False),
        sa.Column("action", sa.String(length=80), nullable=True),
        sa.Column("actor", sa.String(length=120), nullable=True),
        sa.Column("object", sa.String(length=255), nullable=True),
        sa.Column("due_date", sa.Date(), nullable=True),
        sa.Column("temporal_text", sa.String(length=120), nullable=True),
        sa.Column("urgency", sa.String(length=30), nullable=True),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("reasoning_summary", sa.Text(), nullable=True),
        sa.Column("raw_llm_json", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("model_name", sa.String(length=100), nullable=False),
        sa.Column("prompt_version", sa.String(length=30), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["note_id"], ["notes.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("note_id"),
    )
    op.create_index(op.f("ix_note_intents_actor"), "note_intents", ["actor"], unique=False)
    op.create_index(op.f("ix_note_intents_intent_type"), "note_intents", ["intent_type"], unique=False)
    op.create_index(op.f("ix_note_intents_note_id"), "note_intents", ["note_id"], unique=False)
    op.create_index(op.f("ix_note_intents_user_id"), "note_intents", ["user_id"], unique=False)

    op.create_table(
        "intent_category_embeddings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("intent_category_id", sa.Integer(), nullable=False),
        sa.Column("embedding_model", sa.String(length=100), nullable=False),
        sa.Column("embedding_vector", pgvector.sqlalchemy.vector.VECTOR(dim=384), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["intent_category_id"], ["intent_categories.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("intent_category_id"),
    )

    op.create_table(
        "note_intent_assignments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("note_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("intent_category_id", sa.Integer(), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("assignment_method", sa.String(length=50), nullable=False),
        sa.Column("is_primary", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["intent_category_id"], ["intent_categories.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["note_id"], ["notes.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_note_intent_assignments_intent_category_id"), "note_intent_assignments", ["intent_category_id"], unique=False)
    op.create_index(op.f("ix_note_intent_assignments_note_id"), "note_intent_assignments", ["note_id"], unique=False)
    op.create_index(op.f("ix_note_intent_assignments_user_id"), "note_intent_assignments", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_note_intent_assignments_user_id"), table_name="note_intent_assignments")
    op.drop_index(op.f("ix_note_intent_assignments_note_id"), table_name="note_intent_assignments")
    op.drop_index(op.f("ix_note_intent_assignments_intent_category_id"), table_name="note_intent_assignments")
    op.drop_table("note_intent_assignments")
    op.drop_table("intent_category_embeddings")
    op.drop_index(op.f("ix_note_intents_user_id"), table_name="note_intents")
    op.drop_index(op.f("ix_note_intents_note_id"), table_name="note_intents")
    op.drop_index(op.f("ix_note_intents_intent_type"), table_name="note_intents")
    op.drop_index(op.f("ix_note_intents_actor"), table_name="note_intents")
    op.drop_table("note_intents")
    op.drop_index(op.f("ix_intent_categories_user_id"), table_name="intent_categories")
    op.drop_index(op.f("ix_intent_categories_intent_type"), table_name="intent_categories")
    op.drop_index(op.f("ix_intent_categories_actor"), table_name="intent_categories")
    op.drop_table("intent_categories")
