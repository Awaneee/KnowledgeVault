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


class IntentCategoryEmbedding(Base):
    __tablename__ = "intent_category_embeddings"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    intent_category_id: Mapped[int] = mapped_column(
        ForeignKey("intent_categories.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )

    embedding_model: Mapped[str] = mapped_column(
        String(100),
        default="all-MiniLM-L6-v2",
        nullable=False
    )

    embedding_vector = mapped_column(
        Vector(384),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    intent_category = relationship(
        "IntentCategory",
        back_populates="embedding"
    )
