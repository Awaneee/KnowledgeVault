from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import func

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database.base import Base
from app.models.classification_feedback import ClassificationFeedback
from app.models.evaluation_dataset import EvaluationDataset


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        server_default="false",
    )

    verification_token: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
        unique=True,
        index=True,
    )

    reset_token_hash: Mapped[str | None] = mapped_column(
        String(128),
        nullable=True,
        index=True,
    )

    reset_token_expires_at: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    categories = relationship(
        "Category",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    notes = relationship(
        "Note",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    feedbacks = relationship(
        "ClassificationFeedback",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    evaluation_records = relationship(
        "EvaluationDataset",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    intent_categories = relationship(
        "IntentCategory",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    conversations = relationship(
        "ConversationSession",
        back_populates="user",
        cascade="all, delete-orphan",
    )
