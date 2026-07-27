# app/database/base_all.py

from app.database.base import Base

from app.models.user import User
from app.models.category import Category
from app.models.notes import Note
from app.models.attachment import Attachment

from app.models.embedding import Embedding
from app.models.category_embedding import CategoryEmbedding
from app.models.classification_feedback import ClassificationFeedback
from app.models.evaluation_dataset import EvaluationDataset 
from app.models.document_chunk import DocumentChunk
from app.models.chunk_embedding import ChunkEmbedding
from app.models.intent_category import IntentCategory
from app.models.intent_category_embedding import IntentCategoryEmbedding
from app.models.note_intent import NoteIntent
from app.models.note_intent_assignment import NoteIntentAssignment
