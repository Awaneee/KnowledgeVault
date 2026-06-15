from sqlalchemy.orm import Session

from app.core.embedding_model import embedding_model
from app.repositories.embedding_repository import EmbeddingRepository
from app.services.cache_service import CacheService


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

    def search_notes(
        self,
        query: str,
        user_id: int,
        limit: int = 5
    ):
        cache_key = (
            f"semantic_search:"
            f"{user_id}:"
            f"{query.lower()}"
        )

        cached_result = CacheService.get(
            cache_key
        )

        if cached_result:
            print("CACHE HIT")
            return cached_result

        print("CACHE MISS")

        query_vector = embedding_model.encode(
            query
        ).tolist()

        notes = self.repo.search_similar_notes(
            query_vector=query_vector,
            user_id=user_id,
            limit=limit
        )

        response = [
            {
                "id": note.id,
                "title": note.title,
                "content": note.content
            }
            for note in notes
        ]

        CacheService.set(
            cache_key,
            response
        )

        return response

    def get_related_notes(
        self,
        note_id: int,
        user_id: int,
        limit: int = 5
    ):
        notes = self.repo.get_related_notes(
            note_id=note_id,
            user_id=user_id,
            limit=limit
        )

        return [
            {
                "id": note.id,
                "title": note.title,
                "content": note.content
            }
            for note in notes
        ]