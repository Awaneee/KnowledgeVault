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