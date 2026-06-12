# app/models/classification_feedback.py

from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class ClassificationFeedback(Base):
    __tablename__ = "classification_feedback"

    id = Column(Integer, primary_key=True, index=True)
    note_id = Column(Integer, ForeignKey("notes.id", ondelete="CASCADE"), nullable=False)
    predicted_category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    corrected_category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    confidence_score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    note = relationship("Note", backref="feedbacks")
    predicted_category = relationship("Category", foreign_keys=[predicted_category_id])
    corrected_category = relationship("Category", foreign_keys=[corrected_category_id])