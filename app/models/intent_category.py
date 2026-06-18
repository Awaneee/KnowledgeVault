from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database.base import Base


class IntentCategory(Base):
    __tablename__ = "intent_categories"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(120),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    intent_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True
    )

    actor: Mapped[str | None] = mapped_column(
        String(120),
        nullable=True,
        index=True
    )

    action: Mapped[str | None] = mapped_column(
        String(80),
        nullable=True
    )

    time_scope: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="active",
        nullable=False
    )

    source: Mapped[str] = mapped_column(
        String(50),
        default="system_generated",
        nullable=False
    )

    confidence: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False
    )

    note_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    last_used_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    user = relationship(
        "User",
        back_populates="intent_categories"
    )

    assignments = relationship(
        "NoteIntentAssignment",
        back_populates="intent_category",
        cascade="all, delete-orphan"
    )

    embedding = relationship(
        "IntentCategoryEmbedding",
        back_populates="intent_category",
        uselist=False,
        cascade="all, delete-orphan"
    )
