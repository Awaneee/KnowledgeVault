# app/models/embedding.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base  # adjust import to your project's Base location


class Embedding(Base):
    __tablename__ = "embeddings"

    id = Column(Integer, primary_key=True, index=True)
    note_id = Column(Integer, ForeignKey("notes.id", ondelete="CASCADE"), unique=True, nullable=False)
    embedding_model = Column(String(100), nullable=False, default="tfidf-cosine")
    embedding_vector = Column(JSON, nullable=False)          # List[float] stored as JSON
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship back to Note (assumes Note model exists)
    note = relationship("Note", back_populates="embedding")