from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy import DateTime
from sqlalchemy import func

from sqlalchemy.orm import relationship

from app.database.base import Base


class Note(Base):
    __tablename__ = "notes"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(
        String,
        nullable=False
    )

    content = Column(
        Text,
        nullable=True
    )

    source_type = Column(
        String,
        nullable=False,
        default="manual_note"
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    category_id = Column(
        Integer,
        ForeignKey("categories.id"),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    user = relationship(
        "User",
        back_populates="notes"
    )

    category = relationship(
        "Category",
        back_populates="notes"
    )

    attachments = relationship(
        "Attachment",
        back_populates="note",
        cascade="all, delete-orphan"
    )

    embedding = relationship(
        "Embedding",
        back_populates="note",
        uselist=False,
        cascade="all, delete-orphan"
    )

    # Chunk-based retrieval: one note → many chunks
    chunks = relationship(
        "DocumentChunk",
        back_populates="note",
        cascade="all, delete-orphan",
        order_by="DocumentChunk.chunk_index"
    )
