from sqlalchemy.orm import Session

from app.core.embedding_model import embedding_model
from app.repositories.chunk_repository import ChunkRepository
from app.repositories.chunk_embedding_repository import ChunkEmbeddingRepository
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
