import logging

from sqlalchemy.orm import Session

from app.models.conversation import ConversationMessage, ConversationSession

logger = logging.getLogger(__name__)

# Keep at most this many recent messages in the multi-turn prompt window.
HISTORY_WINDOW = 10


class ConversationRepository:

    def __init__(self, db: Session) -> None:
        self.db = db

    # ------------------------------------------------------------------
    # Sessions
    # ------------------------------------------------------------------

    def create_session(self, user_id: int, title: str | None = None) -> ConversationSession:
        session = ConversationSession(user_id=user_id, title=title)
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def get_session(self, session_id: int, user_id: int) -> ConversationSession | None:
        return (
            self.db.query(ConversationSession)
            .filter(
                ConversationSession.id == session_id,
                ConversationSession.user_id == user_id,
            )
            .first()
        )

    def list_sessions(self, user_id: int, limit: int = 20) -> list[ConversationSession]:
        return (
            self.db.query(ConversationSession)
            .filter(ConversationSession.user_id == user_id)
            .order_by(ConversationSession.updated_at.desc())
            .limit(limit)
            .all()
        )

    def update_session_title(self, session: ConversationSession, title: str) -> None:
        session.title = title
        self.db.commit()

    def delete_session(self, session: ConversationSession) -> None:
        self.db.delete(session)
        self.db.commit()

    # ------------------------------------------------------------------
    # Messages
    # ------------------------------------------------------------------

    def add_message(
        self,
        session_id: int,
        role: str,
        content: str,
        citations: list | None = None,
    ) -> ConversationMessage:
        msg = ConversationMessage(
            session_id=session_id,
            role=role,
            content=content,
            citations=citations,
        )
        self.db.add(msg)
        self.db.commit()
        self.db.refresh(msg)
        return msg

    def get_recent_messages(
        self, session_id: int, limit: int = HISTORY_WINDOW
    ) -> list[ConversationMessage]:
        return (
            self.db.query(ConversationMessage)
            .filter(ConversationMessage.session_id == session_id)
            .order_by(ConversationMessage.id.desc())
            .limit(limit)
            .all()[::-1]  # reverse so oldest-first for prompt construction
        )

    def count_messages(self, session_id: int) -> int:
        return (
            self.db.query(ConversationMessage)
            .filter(ConversationMessage.session_id == session_id)
            .count()
        )
