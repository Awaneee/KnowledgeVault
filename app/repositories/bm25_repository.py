"""
BM25 sparse retrieval repository.

Wraps PostgreSQL full-text search (tsvector / tsquery) to provide a BM25-like
ranking signal via ts_rank_cd.  The search_vector column on document_chunks is
maintained automatically by a database trigger (migration c8d9e0f1a2b3).

Why ts_rank_cd?
    ts_rank_cd uses cover density — it rewards documents where query terms
    appear close together, which improves precision on short personal notes.
    Standard ts_rank normalises by document length, but cd gives a better
    signal on our corpus where notes vary wildly in length.

Why websearch_to_tsquery?
    It parses natural-language search strings the same way Google does:
    quoted phrases become phrase queries, minus-prefixes become NOT, and
    free words are AND-combined — without throwing on unexpected input.
    plainto_tsquery is used as a fallback for inputs that produce no tsquery.
"""

import logging
from typing import Optional

from sqlalchemy import text
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class BM25Repository:
    """PostgreSQL full-text search over document_chunks.search_vector."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def search(
        self,
        query: str,
        user_id: int,
        limit: int = 20,
    ) -> list[dict]:
        """
        Return BM25-ranked chunk candidates for *query* belonging to *user_id*.

        Each returned dict contains:
            chunk_id    int   — document_chunks.id
            note_id     int   — parent note
            note_title  str
            chunk_text  str
            chunk_index int
            bm25_score  float — ts_rank_cd output (0.0 – 1.0, higher = better)

        Returns an empty list when:
          - the query produces no valid tsquery (all stop-words, empty string)
          - no chunks match the tsquery for this user
        """
        if not query or not query.strip():
            return []

        # websearch_to_tsquery is robust: unrecognised syntax becomes NULL rather
        # than raising, so we guard with COALESCE / plainto_tsquery fallback.
        sql = text("""
            WITH q AS (
                SELECT COALESCE(
                    NULLIF(websearch_to_tsquery('english', :query_text)::text, ''),
                    plainto_tsquery('english', :query_text)::text
                )::tsquery AS tsq
            )
            SELECT
                dc.id           AS chunk_id,
                dc.note_id      AS note_id,
                n.title         AS note_title,
                dc.chunk_text   AS chunk_text,
                dc.chunk_index  AS chunk_index,
                ts_rank_cd(dc.search_vector, q.tsq) AS bm25_score
            FROM document_chunks dc
            JOIN notes n ON n.id = dc.note_id
            CROSS JOIN q
            WHERE n.user_id   = :user_id
              AND dc.search_vector @@ q.tsq
            ORDER BY bm25_score DESC, dc.id
            LIMIT :limit
        """)

        try:
            rows = self.db.execute(
                sql,
                {"query_text": query.strip(), "user_id": user_id, "limit": limit},
            ).fetchall()
        except Exception:
            logger.exception("BM25 search failed for query=%r user_id=%d", query, user_id)
            return []

        return [
            {
                "chunk_id":    row.chunk_id,
                "note_id":     row.note_id,
                "note_title":  row.note_title,
                "chunk_text":  row.chunk_text,
                "chunk_index": row.chunk_index,
                "bm25_score":  float(row.bm25_score),
            }
            for row in rows
        ]
