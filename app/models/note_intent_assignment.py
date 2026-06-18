from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database.base import Base


class NoteIntentAssignment(Base):
    __tablename__ = "note_intent_assignments"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    note_id: Mapped[int] = mapped_column(
        ForeignKey("notes.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    intent_category_id: Mapped[int] = mapped_column(
        ForeignKey("intent_categories.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    confidence: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False
    )

    assignment_method: Mapped[str] = mapped_column(
        String(50),
        default="hybrid",
        nullable=False
    )

    is_primary: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
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
        back_populates="intent_assignments"
    )

    intent_category = relationship(
        "IntentCategory",
        back_populates="assignments"
    )
