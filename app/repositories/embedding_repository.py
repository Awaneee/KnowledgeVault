from sqlalchemy.orm import Session

from app.models.embedding import Embedding
from app.models.notes import Note


class EmbeddingRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_embedding(
        self,
        note_id: int,
        embedding_model: str,
        embedding_vector: list[float]
    ) -> Embedding:

        embedding = Embedding(
            note_id=note_id,
            embedding_model=embedding_model,
            embedding_vector=embedding_vector
        )

        self.db.add(embedding)
        self.db.commit()
        self.db.refresh(embedding)

        return embedding

    def search_similar_notes(
        self,
        query_vector: list[float],
        user_id: int,
        limit: int = 5
    ) -> list[Note]:

        return (
            self.db.query(Note)
            .join(Embedding)
            .filter(Note.user_id == user_id)
            .order_by(
                Embedding.embedding_vector.cosine_distance(
                    query_vector
                )
            )
            .limit(limit)
            .all()
        )

    def get_related_notes(
        self,
        note_id: int,
        user_id: int,
        limit: int = 5
    ) -> list[Note]:

        source_embedding = (
            self.db.query(Embedding)
            .filter(
                Embedding.note_id == note_id
            )
            .first()
        )

        if not source_embedding:
            return []

        return (
            self.db.query(Note)
            .join(Embedding)
            .filter(
                Note.user_id == user_id,
                Note.id != note_id
            )
            .order_by(
                Embedding.embedding_vector.cosine_distance(
                    source_embedding.embedding_vector
                )
            )
            .limit(limit)
            .all()
        )