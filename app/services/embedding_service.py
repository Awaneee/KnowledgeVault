from sqlalchemy.orm import Session

from app.core.embedding_model import embedding_model
from app.repositories.embedding_repository import EmbeddingRepository


class EmbeddingService:
    MODEL_NAME = "all-MiniLM-L6-v2"

    def __init__(self, db: Session):
        self.db = db
        self.repo = EmbeddingRepository(db)

    def generate_and_store(
        self,
        note_id: int,
        text: str
    ):
        vector = embedding_model.encode(
            text
        ).tolist()

        return self.repo.create_embedding(
            note_id=note_id,
            embedding_model=self.MODEL_NAME,
            embedding_vector=vector
        )