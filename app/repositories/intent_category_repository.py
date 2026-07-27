from datetime import datetime

from sqlalchemy import func
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
            query = query.filter(
                func.lower(IntentCategory.actor) == actor.lower()
            )
        else:
            query = query.filter(IntentCategory.actor.is_(None))
            # If no actor is specified, we must only match generic categories
            # to prevent returning a specific topic category (like "Study - PostgreSQL")
            # as a general fallback rule match.
            generic_categories = {
                "communication", "study", "reference", "ideas", "tasks",
                "reminders", "questions", "meetings", "general",
                "shopping", "bills", "appointments", "errands", "health",
                "finance", "travel"
            }
            query = query.filter(func.lower(IntentCategory.name).in_(generic_categories))

        return (
            query
            .order_by(
                IntentCategory.note_count.desc(),
                IntentCategory.id
            )
            .first()
        )

    def find_by_name(
        self,
        user_id: int,
        name: str,
        intent_type: str | None = None
    ) -> IntentCategory | None:
        query = (
            self.db.query(IntentCategory)
            .filter(
                IntentCategory.user_id == user_id,
                IntentCategory.name == name,
                IntentCategory.status == "active"
            )
        )

        if intent_type:
            query = query.filter(IntentCategory.intent_type == intent_type)

        return (
            query
            .order_by(
                IntentCategory.note_count.desc(),
                IntentCategory.id
            )
            .first()
        )

    def search_by_embedding(
        self,
        user_id: int,
        query_vector: list[float],
        limit: int = 3,
        max_distance: float | None = None
    ) -> list[IntentCategory]:
        """
        Return up to `limit` active categories ordered by cosine distance
        (ascending — nearest first) to `query_vector`.

        `max_distance` is an optional cosine-distance cutoff.
        Cosine distance is in [0, 2]; typical English text pairs cluster:
          < 0.20  near-paraphrase
          0.20–0.40  same topic, different phrasing
          0.40–0.60  related domain, loose overlap
          0.60–0.80  different topics with shared vocabulary
          > 0.80  essentially unrelated

        Earlier query signatures were single words ("todo",
        "general") whose embeddings matched category embeddings at
        distances of ~0.15–0.30 purely by token overlap — the wrong
        categories won, but they looked confident. Richer signatures
        ("todo buy groceries") let the threshold separate genuine matches
        from noise.

        When `max_distance` is provided, any candidate whose cosine
        distance exceeds it is excluded from results.  If no candidate
        clears the threshold, an empty list is returned — the caller
        should treat this as "no matching category" and either create a
        new one (_find_or_create_category) or fall back to semantic
        retrieval (find_categories_for_query).

        Default is None (no threshold, preserves original behaviour) so
        callers that do not pass the argument are completely unaffected.
        Callers that want threshold filtering pass it explicitly; the
        constant IntentCategoryService.CATEGORY_SIMILARITY_THRESHOLD is
        the single place to tune the value.
        """
        base_query = (
            self.db.query(IntentCategory)
            .join(IntentCategoryEmbedding)
            .filter(
                IntentCategory.user_id == user_id,
                IntentCategory.status == "active"
            )
            .order_by(
                IntentCategoryEmbedding.embedding_vector.cosine_distance(
                    query_vector
                ),
                IntentCategory.id
            )
        )

        if max_distance is not None:
            # pgvector exposes the distance expression via the ORM through
            # the column operator; we filter on it directly so the
            # threshold cut happens in Postgres and no extra rows are
            # fetched and then discarded in Python.
            base_query = base_query.filter(
                IntentCategoryEmbedding.embedding_vector.cosine_distance(
                    query_vector
                ) <= max_distance
            )

        return base_query.limit(limit).all()

    def search_by_embedding_with_distance(
        self,
        user_id: int,
        query_vector: list[float],
        limit: int = 3,
        max_distance: float | None = None,
        intent_type: str | None = None,
        actor: str | None = None,
    ) -> list[tuple[IntentCategory, float]]:
        distance_expr = IntentCategoryEmbedding.embedding_vector.cosine_distance(
            query_vector
        )
        distance = distance_expr.label("distance")

        query = (
            self.db.query(
                IntentCategory,
                distance
            )
            .join(IntentCategoryEmbedding)
            .filter(
                IntentCategory.user_id == user_id,
                IntentCategory.status == "active"
            )
        )

        if max_distance is not None:
            query = query.filter(distance_expr <= max_distance)

        if intent_type is not None:
            query = query.filter(IntentCategory.intent_type == intent_type)

        if actor is not None:
            query = query.filter(func.lower(IntentCategory.actor) == actor.lower())

        return (
            query
            .order_by(
                distance_expr,
                IntentCategory.id
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
        # DB safety truncation
        safe_name = (name or "General")[:120]
        
        valid_types = {
            "communication", "todo", "study", "reminder",
            "idea", "reference", "question", "event", "general"
        }
        safe_intent_type = intent_type if intent_type in valid_types else "general"

        category = IntentCategory(
            user_id=user_id,
            name=safe_name,
            intent_type=safe_intent_type,
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

    def get_embedding(
        self,
        intent_category_id: int,
    ) -> IntentCategoryEmbedding | None:
        return (
            self.db.query(IntentCategoryEmbedding)
            .filter(
                IntentCategoryEmbedding.intent_category_id == intent_category_id
            )
            .first()
        )

    def upsert_embedding(
        self,
        intent_category_id: int,
        embedding_model: str,
        embedding_vector: list[float],
        centroid_note_count: int = 1,
    ) -> IntentCategoryEmbedding:
        embedding = self.get_embedding(intent_category_id)

        if not embedding:
            embedding = IntentCategoryEmbedding(
                intent_category_id=intent_category_id,
                embedding_model=embedding_model,
                embedding_vector=embedding_vector,
                centroid_note_count=centroid_note_count,
            )
            self.db.add(embedding)
        else:
            embedding.embedding_model = embedding_model
            embedding.embedding_vector = embedding_vector
            embedding.centroid_note_count = centroid_note_count

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

    def count_by_user(self, user_id: int) -> int:
        # Only active categories count against the cap; archived/merged ones
        # have already been removed from the browsing and retrieval paths.
        return (
            self.db.query(IntentCategory)
            .filter(
                IntentCategory.user_id == user_id,
                IntentCategory.status == "active",
            )
            .count()
        )
