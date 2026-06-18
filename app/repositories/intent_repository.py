from datetime import datetime

from sqlalchemy.orm import Session

from app.models.note_intent import NoteIntent
from app.models.note_intent_assignment import NoteIntentAssignment
from app.models.notes import Note


class IntentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_or_update_note_intent(
        self,
        note_id: int,
        user_id: int,
        data: dict
    ) -> NoteIntent:
        intent = (
            self.db.query(NoteIntent)
            .filter(NoteIntent.note_id == note_id)
            .first()
        )

        if not intent:
            intent = NoteIntent(
                note_id=note_id,
                user_id=user_id
            )
            self.db.add(intent)

        for field in [
            "intent_type",
            "action",
            "actor",
            "object",
            "due_date",
            "temporal_text",
            "urgency",
            "confidence",
            "reasoning_summary",
            "raw_llm_json",
            "model_name",
            "prompt_version"
        ]:
            if field in data:
                setattr(intent, field, data[field])

        intent.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(intent)
        return intent

    def create_or_update_assignment(
        self,
        note_id: int,
        user_id: int,
        intent_category_id: int,
        confidence: float,
        assignment_method: str
    ) -> NoteIntentAssignment:
        assignment = (
            self.db.query(NoteIntentAssignment)
            .filter(
                NoteIntentAssignment.note_id == note_id,
                NoteIntentAssignment.is_primary.is_(True)
            )
            .first()
        )

        if not assignment:
            assignment = NoteIntentAssignment(
                note_id=note_id,
                user_id=user_id,
                is_primary=True
            )
            self.db.add(assignment)

        assignment.intent_category_id = intent_category_id
        assignment.confidence = confidence
        assignment.assignment_method = assignment_method
        assignment.updated_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(assignment)
        return assignment

    def get_note_intent(
        self,
        note_id: int,
        user_id: int
    ) -> NoteIntent | None:
        return (
            self.db.query(NoteIntent)
            .filter(
                NoteIntent.note_id == note_id,
                NoteIntent.user_id == user_id
            )
            .first()
        )

    def get_notes_for_category(
        self,
        intent_category_id: int,
        user_id: int
    ) -> list[Note]:
        return (
            self.db.query(Note)
            .join(
                NoteIntentAssignment,
                NoteIntentAssignment.note_id == Note.id
            )
            .filter(
                Note.user_id == user_id,
                NoteIntentAssignment.intent_category_id == intent_category_id
            )
            .order_by(Note.updated_at.desc())
            .all()
        )
