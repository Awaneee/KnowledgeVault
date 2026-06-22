from sqlalchemy.orm import Session

from app.core.embedding_model import embedding_model
from app.repositories.chunk_repository import ChunkRepository
from app.repositories.chunk_embedding_repository import ChunkEmbeddingRepository
from app.services.intent_category_service import IntentCategoryService
from app.services.chunking_service import ChunkingService


class ChunkService:
    """
    Orchestrates the full chunk pipeline for a single note:
        text → chunks → store chunks → generate embeddings → store embeddings

    Deliberately kept separate from NoteService so each service
    retains a single responsibility.
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
        """
        Chunk *text*, persist chunks and their embeddings for
        *note_id*.  Returns the number of chunks created.
        """
        chunk_texts = ChunkingService.split(text)

        if not chunk_texts:
            return 0

        # Persist chunks (bulk insert)
        chunks = self.chunk_repo.create_chunks(
            note_id=note_id,
            texts=chunk_texts
        )

        # Encode all chunk texts in one batch call for efficiency
        vectors = embedding_model.encode(
            chunk_texts
        ).tolist()

        # Build bulk-insert payload
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
        Semantic chunk retrieval.

        Returns a list of dicts:
            {
                "chunk_text"  : str,
                "chunk_index" : int,
                "note_title"  : str
            }
        """
        query_vector = embedding_model.encode(query).tolist()

        rows = self.embedding_repo.search_similar_chunks(
            query_vector=query_vector,
            user_id=user_id,
            limit=limit
        )

        return [
            {
                "chunk_text": chunk.chunk_text,
                "chunk_index": chunk.chunk_index,
                "note_title": note_title
            }
            for chunk, note_title in rows
        ]

    def retrieve_hybrid(
        self,
        query: str,
        user_id: int,
        limit: int = 5
    ) -> list[dict]:
        """
        Intent-aware retrieval.

        First pulls chunks from notes whose extracted intent matches
        the query, then fills remaining slots with semantic pgvector
        results. Duplicate chunks are removed by note title/index/text.
        """
        results = []
        seen = set()

        intent_categories = self.intent_category_service.find_categories_for_query(
            query=query,
            user_id=user_id,
            limit=3
        )

        for category in intent_categories:
            notes = self.intent_category_service.get_notes_for_category(
                intent_category_id=category.id,
                user_id=user_id
            )

            for note in notes:
                chunks = self.chunk_repo.get_chunks_by_note(
                    note_id=note.id
                )

                if not chunks:
                    continue

                # Use ALL chunks from the note ranked by chunk_index,
                # not just chunks[0]. Taking only the first chunk meant
                # the RAG system could only ever see the opening of each
                # note regardless of where the relevant content actually
                # was, breaking retrieval for anything beyond the first
                # ~500 characters of a note.
                for chunk in sorted(chunks, key=lambda c: c.chunk_index):
                    key = (note.title, chunk.chunk_index, chunk.chunk_text)

                    if key in seen:
                        continue

                    seen.add(key)
                    results.append(
                        {
                            "chunk_text": chunk.chunk_text,
                            "chunk_index": chunk.chunk_index,
                            "note_title": note.title,
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
                item["note_title"],
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
