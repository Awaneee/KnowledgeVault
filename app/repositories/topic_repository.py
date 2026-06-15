from sqlalchemy.orm import Session

from app.models.notes import Note
from app.models.embedding import Embedding


class TopicRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_notes_with_embeddings(
        self,
        user_id: int
    ):
        return (
            self.db.query(Note)
            .join(Embedding)
            .filter(
                Note.user_id == user_id
            )
            .all()
        )