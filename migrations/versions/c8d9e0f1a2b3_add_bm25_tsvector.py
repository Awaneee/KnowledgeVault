"""add BM25 tsvector column for sparse full-text retrieval

Revision ID: c8d9e0f1a2b3
Revises: d4e5f6a7b8c9
Create Date: 2026-08-03 00:00:00.000000

Adds a server-maintained tsvector column to document_chunks so PostgreSQL
full-text search (BM25 via ts_rank_cd) can run without touching the Python
application layer.

Schema changes
--------------
- document_chunks.search_vector  tsvector  (nullable, server-maintained)
- GIN index on document_chunks.search_vector
- Trigger function tsvector_update_trigger_fn fires BEFORE INSERT OR UPDATE
  OF chunk_text and sets search_vector = to_tsvector('english', chunk_text).
- Backfill: UPDATE document_chunks SET search_vector = ... for existing rows.

Downgrade rolls back all of the above cleanly.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "c8d9e0f1a2b3"
down_revision: Union[str, Sequence[str], None] = "d4e5f6a7b8c9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Add the tsvector column (nullable so existing rows don't fail).
    op.add_column(
        "document_chunks",
        sa.Column(
            "search_vector",
            postgresql.TSVECTOR(),
            nullable=True,
        ),
    )

    # 2. GIN index — required for @@ queries to be fast at any corpus size.
    op.create_index(
        "ix_document_chunks_search_vector",
        "document_chunks",
        ["search_vector"],
        postgresql_using="gin",
    )

    # 3. Trigger function: auto-update search_vector on insert/update.
    op.execute("""
        CREATE OR REPLACE FUNCTION document_chunks_tsvector_update()
        RETURNS trigger
        LANGUAGE plpgsql
        AS $$
        BEGIN
            NEW.search_vector := to_tsvector('english', COALESCE(NEW.chunk_text, ''));
            RETURN NEW;
        END;
        $$;
    """)

    op.execute("""
        CREATE TRIGGER trg_document_chunks_tsvector
        BEFORE INSERT OR UPDATE OF chunk_text
        ON document_chunks
        FOR EACH ROW
        EXECUTE FUNCTION document_chunks_tsvector_update();
    """)

    # 4. Backfill existing rows — trigger won't fire for already-stored rows.
    op.execute("""
        UPDATE document_chunks
        SET search_vector = to_tsvector('english', COALESCE(chunk_text, ''))
        WHERE search_vector IS NULL;
    """)


def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS trg_document_chunks_tsvector ON document_chunks;")
    op.execute("DROP FUNCTION IF EXISTS document_chunks_tsvector_update();")
    op.drop_index("ix_document_chunks_search_vector", table_name="document_chunks")
    op.drop_column("document_chunks", "search_vector")
