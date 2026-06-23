from sqlalchemy.orm import Session

from app.core.embedding_model import embedding_model
from app.models.intent_category import IntentCategory
from app.models.note_intent import NoteIntent
from app.models.notes import Note
from app.repositories.intent_category_repository import IntentCategoryRepository
from app.repositories.intent_repository import IntentRepository
from app.services.intent_extraction_service import IntentExtractionService


class IntentCategoryService:
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"

    def __init__(self, db: Session):
        self.db = db
        self.category_repo = IntentCategoryRepository(db)
        self.intent_repo = IntentRepository(db)
        self.extractor = IntentExtractionService()

    def process_note(
        self,
        note_id: int,
        user_id: int,
        title: str,
        content: str | None
    ) -> dict:
        intent = self.extractor.extract(
            title=title,
            content=content
        )

        stored_intent = self.intent_repo.create_or_update_note_intent(
            note_id=note_id,
            user_id=user_id,
            data=intent
        )

        category, method = self._find_or_create_category(
            user_id=user_id,
            intent=intent
        )

        assignment = self.intent_repo.create_or_update_assignment(
            note_id=note_id,
            user_id=user_id,
            intent_category_id=category.id,
            confidence=intent["confidence"],
            assignment_method=method
        )

        self.category_repo.touch_after_assignment(
            category_id=category.id
        )

        self._refresh_category_embedding(
            category=category,
            intent=intent
        )

        return {
            "intent": stored_intent,
            "category": category,
            "assignment": assignment
        }

    def get_categories(
        self,
        user_id: int
    ) -> list[IntentCategory]:
        return self.category_repo.get_all(
            user_id=user_id
        )

    def get_notes_for_category(
        self,
        intent_category_id: int,
        user_id: int
    ):
        return self.intent_repo.get_notes_for_category(
            intent_category_id=intent_category_id,
            user_id=user_id
        )

    def backfill_user_notes(
        self,
        user_id: int,
        limit: int = 100
    ) -> dict:
        notes = (
            self.db.query(Note)
            .outerjoin(NoteIntent, NoteIntent.note_id == Note.id)
            .filter(
                Note.user_id == user_id,
                NoteIntent.id.is_(None)
            )
            .order_by(Note.created_at.asc())
            .limit(limit)
            .all()
        )

        processed = 0
        failed = 0

        for note in notes:
            try:
                self.process_note(
                    note_id=note.id,
                    user_id=user_id,
                    title=note.title,
                    content=note.content
                )
                processed += 1
            except Exception:
                self.db.rollback()
                failed += 1

        remaining = (
            self.db.query(Note)
            .outerjoin(NoteIntent, NoteIntent.note_id == Note.id)
            .filter(
                Note.user_id == user_id,
                NoteIntent.id.is_(None)
            )
            .count()
        )

        return {
            "processed": processed,
            "failed": failed,
            "remaining_hint": remaining
        }

    def find_categories_for_query(
        self,
        query: str,
        user_id: int,
        limit: int = 3
    ) -> list[IntentCategory]:
        # Query-time path: no LLM call. extract_query_intent_fast() is a
        # pure keyword classifier (sub-millisecond). The Phi3-backed
        # extract_query_intent() is intentionally NOT used here — it was
        # the source of the ~60-70s Ask retrieval latency. Note creation
        # (process_note -> self.extractor.extract) still uses the LLM
        # and is unaffected by this change, since it runs in the
        # background Redis worker, not on the request path.
        intent = self.extractor.extract_query_intent_fast(query)

        exact = self.category_repo.find_rule_match(
            user_id=user_id,
            intent_type=intent["intent_type"],
            actor=intent["actor"]
        )

        if exact:
            return [exact]

        vector = embedding_model.encode(
            self._intent_signature(intent)
        ).tolist()

        return self.category_repo.search_by_embedding(
            user_id=user_id,
            query_vector=vector,
            limit=limit
        )

    # Maximum number of intent categories a single user can have.
    # Without a cap, every unique actor/intent combination creates a
    # new category indefinitely. At scale this produces hundreds of
    # near-duplicate categories ("Work Tasks", "Work Items", etc.)
    # that degrade retrieval quality and slow category search queries.
    # When the cap is reached we fall back to the closest vector match
    # regardless of the compatibility check, so notes still get
    # categorized - just into the best existing bucket rather than a
    # new one.
    MAX_CATEGORIES_PER_USER = 50

    def _find_or_create_category(
        self,
        user_id: int,
        intent: dict
    ) -> tuple[IntentCategory, str]:
        category = self.category_repo.find_rule_match(
            user_id=user_id,
            intent_type=intent["intent_type"],
            actor=intent["actor"]
        )

        if category:
            return category, "exact_rule"

        if intent["confidence"] >= 0.68:
            vector = embedding_model.encode(
                self._intent_signature(intent)
            ).tolist()

            candidates = self.category_repo.search_by_embedding(
                user_id=user_id,
                query_vector=vector,
                limit=1
            )

            if candidates:
                candidate = candidates[0]
                if self._compatible(candidate, intent):
                    return candidate, "vector"

        # Check category count before creating a new one.
        # If the user is at or above the cap, reuse the closest vector
        # match (even if not perfectly compatible) rather than creating
        # another category that pushes the total higher.
        current_count = self.category_repo.count_by_user(user_id)
        if current_count >= self.MAX_CATEGORIES_PER_USER:
            vector = embedding_model.encode(
                self._intent_signature(intent)
            ).tolist()

            fallback = self.category_repo.search_by_embedding(
                user_id=user_id,
                query_vector=vector,
                limit=1
            )

            if fallback:
                return fallback[0], "cap_fallback"

        name = self._generate_category_name(intent)
        description = self._generate_description(intent)

        category = self.category_repo.create(
            user_id=user_id,
            name=name,
            intent_type=intent["intent_type"],
            actor=intent["actor"],
            action=intent["action"],
            time_scope=self._time_scope(intent),
            description=description,
            confidence=intent["confidence"]
        )

        return category, "created"

    def _compatible(
        self,
        category: IntentCategory,
        intent: dict
    ) -> bool:
        if category.intent_type != intent["intent_type"]:
            return False

        if category.actor and intent["actor"]:
            return category.actor.lower() == intent["actor"].lower()

        return category.actor is None and intent["actor"] is None

    def _refresh_category_embedding(
        self,
        category: IntentCategory,
        intent: dict
    ) -> None:
        text = " ".join(
            part
            for part in [
                category.name,
                category.intent_type,
                category.actor,
                category.action,
                intent.get("object")
            ]
            if part
        )

        vector = embedding_model.encode(text).tolist()

        self.category_repo.upsert_embedding(
            intent_category_id=category.id,
            embedding_model=self.EMBEDDING_MODEL,
            embedding_vector=vector
        )

    def _intent_signature(
        self,
        intent: dict
    ) -> str:
        return " ".join(
            part
            for part in [
                intent.get("intent_type"),
                intent.get("action"),
                intent.get("actor"),
                intent.get("object"),
                intent.get("temporal_text")
            ]
            if part
        )

    def _generate_category_name(
        self,
        intent: dict
    ) -> str:
        intent_type = intent["intent_type"]
        actor = intent.get("actor")
        action = intent.get("action")
        obj = intent.get("object")

        if intent_type == "communication" and actor:
            if action == "ask":
                return f"Questions for {actor}"
            return f"Things to Tell {actor}"

        if intent_type == "todo":
            return "To Do"

        if intent_type == "study":
            return "Study Tasks"

        if intent_type == "reminder":
            if obj and "medicine" in obj.lower():
                return "Health Reminders"
            return "Reminders"

        if intent_type == "question":
            return "Questions"

        if intent_type == "idea":
            return "Ideas"

        if intent_type == "reference":
            return "Reference Notes"

        if intent_type == "event":
            return "Events"

        return "General"

    def _generate_description(
        self,
        intent: dict
    ) -> str:
        if intent.get("actor"):
            return (
                f"Notes with {intent['intent_type']} intent "
                f"involving {intent['actor']}."
            )

        return f"Notes with {intent['intent_type']} intent."

    def _time_scope(
        self,
        intent: dict
    ) -> str | None:
        if intent.get("due_date"):
            return "dated"

        temporal_text = intent.get("temporal_text")

        if temporal_text:
            return temporal_text.lower().replace(" ", "_")[:50]

        return None