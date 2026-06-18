from datetime import datetime

from sqlalchemy.orm import Session

from app.models.intent_category import IntentCategory
from app.models.intent_category_embedding import IntentCategoryEmbedding
from app.models.note_intent_assignment import NoteIntentAssignment
from app.models.notes import Note


class IntentCategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(
        self,
        user_id: int
    ) -> list[IntentCategory]:
        return (
            self.db.query(IntentCategory)
            .filter(
                IntentCategory.user_id == user_id,
                IntentCategory.status == "active"
            )
            .order_by(
                IntentCategory.last_used_at.desc().nullslast(),
                IntentCategory.name
            )
            .all()
        )

    def find_rule_match(
        self,
        user_id: int,
        intent_type: str,
        actor: str | None
    ) -> IntentCategory | None:
        query = (
            self.db.query(IntentCategory)
            .filter(
                IntentCategory.user_id == user_id,
                IntentCategory.intent_type == intent_type,
                IntentCategory.status == "active"
            )
        )

        if actor:
            query = query.filter(IntentCategory.actor == actor)
        else:
            query = query.filter(IntentCategory.actor.is_(None))

        return query.order_by(IntentCategory.note_count.desc()).first()

    def search_by_embedding(
        self,
        user_id: int,
        query_vector: list[float],
        limit: int = 3
    ) -> list[IntentCategory]:
        return (
            self.db.query(IntentCategory)
            .join(IntentCategoryEmbedding)
            .filter(
                IntentCategory.user_id == user_id,
                IntentCategory.status == "active"
            )
            .order_by(
                IntentCategoryEmbedding.embedding_vector.cosine_distance(
                    query_vector
                )
            )
            .limit(limit)
            .all()
        )

    def create(
        self,
        user_id: int,
        name: str,
        intent_type: str,
        actor: str | None,
        action: str | None,
        time_scope: str | None,
        description: str | None,
        confidence: float,
        source: str = "system_generated"
    ) -> IntentCategory:
        category = IntentCategory(
            user_id=user_id,
            name=name,
            intent_type=intent_type,
            actor=actor,
            action=action,
            time_scope=time_scope,
            description=description,
            confidence=confidence,
            source=source,
            note_count=0,
            last_used_at=datetime.utcnow()
        )
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def touch_after_assignment(
        self,
        category_id: int
    ) -> None:
        note_count = (
            self.db.query(NoteIntentAssignment)
            .filter(NoteIntentAssignment.intent_category_id == category_id)
            .count()
        )

        category = (
            self.db.query(IntentCategory)
            .filter(IntentCategory.id == category_id)
            .first()
        )

        if category:
            category.note_count = note_count
            category.last_used_at = datetime.utcnow()
            category.updated_at = datetime.utcnow()
            self.db.commit()

    def upsert_embedding(
        self,
        intent_category_id: int,
        embedding_model: str,
        embedding_vector: list[float]
    ) -> IntentCategoryEmbedding:
        embedding = (
            self.db.query(IntentCategoryEmbedding)
            .filter(
                IntentCategoryEmbedding.intent_category_id == intent_category_id
            )
            .first()
        )

        if not embedding:
            embedding = IntentCategoryEmbedding(
                intent_category_id=intent_category_id,
                embedding_model=embedding_model,
                embedding_vector=embedding_vector
            )
            self.db.add(embedding)
        else:
            embedding.embedding_model = embedding_model
            embedding.embedding_vector = embedding_vector

        self.db.commit()
        self.db.refresh(embedding)
        return embedding

    def get_notes_for_intent_categories(
        self,
        user_id: int,
        intent_category_ids: list[int],
        limit: int
    ) -> list[Note]:
        if not intent_category_ids:
            return []

        return (
            self.db.query(Note)
            .join(
                NoteIntentAssignment,
                NoteIntentAssignment.note_id == Note.id
            )
            .filter(
                Note.user_id == user_id,
                NoteIntentAssignment.intent_category_id.in_(intent_category_ids)
            )
            .order_by(Note.updated_at.desc())
            .limit(limit)
            .all()
        )
