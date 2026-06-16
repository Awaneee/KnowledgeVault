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

        Each dict must have:
            chunk_id        : int
            embedding_model : str
            embedding_vector: list[float]
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
    ) -> list[tuple[DocumentChunk, str]]:
        """
        Return the top-k chunks closest to query_vector for a
        given user, along with the parent note title.

        Returns a list of (DocumentChunk, note_title) tuples
        ordered by ascending cosine distance.
        """
        rows = (
            self.db.query(DocumentChunk, Note.title)
            .join(
                ChunkEmbedding,
                ChunkEmbedding.chunk_id == DocumentChunk.id
            )
            .join(
                Note,
                Note.id == DocumentChunk.note_id
            )
            .filter(Note.user_id == user_id)
            .order_by(
                ChunkEmbedding.embedding_vector.cosine_distance(
                    query_vector
                )
            )
            .limit(limit)
            .all()
        )

        return rows   # list of (DocumentChunk, str)
