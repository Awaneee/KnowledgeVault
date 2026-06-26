from sqlalchemy.orm import Session

from app.core.embedding_model import embedding_model
from app.repositories.chunk_repository import ChunkRepository
from app.repositories.chunk_embedding_repository import ChunkEmbeddingRepository
from app.services.intent_category_service import IntentCategoryService
from app.services.chunking_service import ChunkingService


class ChunkService:
    """
    Orchestrates the full chunk pipeline for a single note:

        text
            ↓
        chunks
            ↓
        store chunks
            ↓
        embeddings
            ↓
        store embeddings
    """

    MODEL_NAME = "all-MiniLM-L6-v2"

    def __init__(self, db: Session):
        self.db = db
        self.chunk_repo = ChunkRepository(db)
        self.embedding_repo = ChunkEmbeddingRepository(db)
        self.intent_category_service = IntentCategoryService(db)

    def process_note(
        self,
        note_id: int,
        text: str
    ) -> int:

        chunk_texts = ChunkingService.split(text)

        if not chunk_texts:
            return 0

        chunks = self.chunk_repo.create_chunks(
            note_id=note_id,
            texts=chunk_texts
        )

        vectors = embedding_model.encode(
            chunk_texts
        ).tolist()

        records = [
            {
                "chunk_id": chunk.id,
                "embedding_model": self.MODEL_NAME,
                "embedding_vector": vector
            }
            for chunk, vector in zip(chunks, vectors)
        ]

        self.embedding_repo.bulk_create_embeddings(records)

        return len(chunks)

    def retrieve(
        self,
        query: str,
        user_id: int,
        limit: int = 5
    ) -> list[dict]:
        """
        Pure semantic retrieval.
        """

        query_vector = embedding_model.encode(query).tolist()

        rows = self.embedding_repo.search_similar_chunks(
            query_vector=query_vector,
            user_id=user_id,
            limit=limit
        )

        return [
            {
                "note_id": note.id,
                "note_title": note.title,
                "chunk_text": chunk.chunk_text,
                "chunk_index": chunk.chunk_index
            }
            for chunk, note in rows
        ]

    def retrieve_hybrid(
        self,
        query: str,
        user_id: int,
        limit: int = 5
    ) -> list[dict]:
        """
        Hybrid Retrieval

        Phase 1
            Intent retrieval

        Phase 2
            Semantic retrieval

        Duplicate chunks are removed.
        """

        results = []
        seen = set()

        intent_categories = (
            self.intent_category_service.find_categories_for_query(
                query=query,
                user_id=user_id,
                limit=3
            )
        )

        for category in intent_categories:

            notes = (
                self.intent_category_service.get_notes_for_category(
                    intent_category_id=category.id,
                    user_id=user_id
                )
            )

            for note in notes:

                chunks = self.chunk_repo.get_chunks_by_note(
                    note_id=note.id
                )

                if not chunks:
                    continue

                for chunk in sorted(
                    chunks,
                    key=lambda c: c.chunk_index
                ):

                    key = (
                        note.id,
                        chunk.chunk_index,
                        chunk.chunk_text
                    )

                    if key in seen:
                        continue

                    seen.add(key)

                    results.append(
                        {
                            "note_id": note.id,
                            "note_title": note.title,
                            "chunk_text": chunk.chunk_text,
                            "chunk_index": chunk.chunk_index,
                            "source": "intent",
                            "intent_category": category.name
                        }
                    )

                    if len(results) >= limit:
                        return results

        semantic_results = self.retrieve(
            query=query,
            user_id=user_id,
            limit=limit
        )

        for item in semantic_results:

            key = (
                item["note_id"],
                item["chunk_index"],
                item["chunk_text"]
            )

            if key in seen:
                continue

            seen.add(key)

            item["source"] = "semantic"
            item["intent_category"] = None

            results.append(item)

            if len(results) >= limit:
                break

        return results