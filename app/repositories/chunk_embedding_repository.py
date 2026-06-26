from sqlalchemy.orm import Session

from app.models.chunk_embedding import ChunkEmbedding
from app.models.document_chunk import DocumentChunk
from app.models.notes import Note


class ChunkEmbeddingRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_embedding(
        self,
        chunk_id: int,
        embedding_model: str,
        embedding_vector: list[float]
    ) -> ChunkEmbedding:

        embedding = ChunkEmbedding(
            chunk_id=chunk_id,
            embedding_model=embedding_model,
            embedding_vector=embedding_vector
        )

        self.db.add(embedding)
        self.db.commit()
        self.db.refresh(embedding)

        return embedding

    def bulk_create_embeddings(
        self,
        records: list[dict]
    ) -> list[ChunkEmbedding]:
        """
        Bulk-insert chunk embeddings in one commit.

        Each dict must contain:
            chunk_id
            embedding_model
            embedding_vector
        """

        embeddings = [
            ChunkEmbedding(
                chunk_id=r["chunk_id"],
                embedding_model=r["embedding_model"],
                embedding_vector=r["embedding_vector"]
            )
            for r in records
        ]

        self.db.add_all(embeddings)
        self.db.commit()

        for emb in embeddings:
            self.db.refresh(emb)

        return embeddings

    def search_similar_chunks(
        self,
        query_vector: list[float],
        user_id: int,
        limit: int = 5
    ) -> list[tuple[DocumentChunk, Note]]:
        """
        Returns:

            (
                DocumentChunk,
                Note
            )

        Returning the Note object instead of only the title gives
        downstream services access to:

        - note.id
        - note.title
        - any future metadata

        This is required by the evaluation framework to compute
        Recall@K, Precision@K, MRR, etc.
        """

        rows = (
            self.db.query(
                DocumentChunk,
                Note
            )
            .join(
                ChunkEmbedding,
                ChunkEmbedding.chunk_id == DocumentChunk.id
            )
            .join(
                Note,
                Note.id == DocumentChunk.note_id
            )
            .filter(
                Note.user_id == user_id
            )
            .order_by(
                ChunkEmbedding.embedding_vector.cosine_distance(
                    query_vector
                )
            )
            .limit(limit)
            .all()
        )

        return rows