from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.database.base import Base


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="notes")
    category = relationship("Category", back_populates="notes")
    attachments = relationship("Attachment", back_populates="note", cascade="all, delete-orphan")
    # app/models/note.py  ← ADD this line inside the Note class
    embedding = relationship("Embedding", back_populates="note", uselist=False, cascade="all, delete-orphan")