from datetime import date
from datetime import datetime

from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

from sqlalchemy.dialects.postgresql import JSONB

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database.base import Base


class NoteIntent(Base):
    __tablename__ = "note_intents"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    note_id: Mapped[int] = mapped_column(
        ForeignKey("notes.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    intent_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True
    )

    action: Mapped[str | None] = mapped_column(
        String(80),
        nullable=True
    )

    actor: Mapped[str | None] = mapped_column(
        String(120),
        nullable=True,
        index=True
    )

    topic: Mapped[str | None] = mapped_column(
        String(120),
        nullable=True
    )

    subtopic: Mapped[str | None] = mapped_column(
        String(120),
        nullable=True
    )

    object: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    due_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    temporal_text: Mapped[str | None] = mapped_column(
        String(120),
        nullable=True
    )

    urgency: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True
    )

    confidence: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False
    )

    extraction_quality_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    reasoning_summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    raw_llm_json: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True
    )

    model_name: Mapped[str] = mapped_column(
        String(100),
        default="llama3:latest",
        nullable=False
    )

    prompt_version: Mapped[str] = mapped_column(
        String(30),
        default="intent-v1",
        nullable=False
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

    note = relationship(
        "Note",
        back_populates="intent"
    )
