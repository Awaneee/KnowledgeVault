from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunk


class ChunkRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_chunks(
        self,
        note_id: int,
        texts: list[str]
    ) -> list[DocumentChunk]:
        """
        Bulk-insert all chunks for a note in a single commit.
        Returns the persisted DocumentChunk instances in order.
        """
        chunks = [
            DocumentChunk(
                note_id=note_id,
                chunk_text=text,
                chunk_index=index
            )
            for index, text in enumerate(texts)
        ]

        self.db.add_all(chunks)
        self.db.commit()

        for chunk in chunks:
            self.db.refresh(chunk)

        return chunks

    def get_chunks_by_note(
        self,
        note_id: int
    ) -> list[DocumentChunk]:
        return (
            self.db.query(DocumentChunk)
            .filter(DocumentChunk.note_id == note_id)
            .order_by(DocumentChunk.chunk_index)
            .all()
        )

    def get_chunk_by_id(
        self,
        chunk_id: int
    ) -> DocumentChunk | None:
        return (
            self.db.query(DocumentChunk)
            .filter(DocumentChunk.id == chunk_id)
            .first()
        )
