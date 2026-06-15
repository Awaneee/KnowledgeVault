from datetime import datetime

from pgvector.sqlalchemy import Vector

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database.base import Base


class Embedding(Base):
    __tablename__ = "embeddings"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    note_id: Mapped[int] = mapped_column(
        ForeignKey("notes.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )

    embedding_model: Mapped[str] = mapped_column(
        String(100),
        default="all-MiniLM-L6-v2"
    )

    embedding_vector = mapped_column(
        Vector(384),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    note = relationship(
        "Note",
        back_populates="embedding"
    )