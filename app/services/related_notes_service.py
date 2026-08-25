"""
Related notes service — finds semantically similar notes using pgvector cosine distance.

For a given note, fetches its stored embedding vector then queries the embeddings
table for the closest neighbours (by cosine distance) that belong to the same user.
Returns results ranked by similarity (1 = identical, 0 = orthogonal).
"""

import logging

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.models.embedding import Embedding
from app.models.notes import Note

logger = logging.getLogger(__name__)

_DEFAULT_LIMIT = 5
_MAX_LIMIT = 20


class RelatedNotesService:

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_related(
        self, note_id: int, user_id: int, limit: int = _DEFAULT_LIMIT
    ) -> list[dict]:
        limit = min(limit, _MAX_LIMIT)

        # Fetch the source note's embedding vector.
        source = (
            self.db.query(Embedding)
            .join(Note, Note.id == Embedding.note_id)
            .filter(Embedding.note_id == note_id, Note.user_id == user_id)
            .first()
        )
        if source is None:
            logger.info("RELATED note_id=%d has no embedding yet", note_id)
            return []

        # pgvector cosine distance operator: <=> (lower = more similar).
        # Cast the Python list to a vector literal so SQLAlchemy sends the
        # right type without needing ORM-level vector column binds.
        vector_str = "[" + ",".join(str(v) for v in source.embedding_vector) + "]"

        rows = self.db.execute(
            text(
                """
                SELECT
                    n.id          AS note_id,
                    n.title       AS title,
                    LEFT(n.content, 200) AS snippet,
                    1 - (e.embedding_vector <=> CAST(:vec AS vector)) AS similarity
                FROM embeddings e
                JOIN notes n ON n.id = e.note_id
                WHERE n.user_id = :user_id
                  AND e.note_id != :note_id
                ORDER BY e.embedding_vector <=> CAST(:vec AS vector)
                LIMIT :limit
                """
            ),
            {"vec": vector_str, "user_id": user_id, "note_id": note_id, "limit": limit},
        ).fetchall()

        return [
            {
                "note_id": r.note_id,
                "title": r.title,
                "snippet": r.snippet or "",
                "similarity": round(float(r.similarity), 4),
            }
            for r in rows
        ]
