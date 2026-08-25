"""
Conversation service — wraps AskService with persistent multi-turn memory.

Each conversation session keeps an ordered list of messages.  On each new
turn the service:

  1. Loads the most recent HISTORY_WINDOW messages from the session.
  2. Builds a conversation history prefix that is prepended to the retrieval
     prompt so the LLM understands follow-up context ("it" / "that" / "the
     one you mentioned" all resolve correctly).
  3. Calls the core ask pipeline with the enriched prompt.
  4. Persists both the user turn and the assistant response to the DB.

Auto-titling: the first user message in a new session becomes the session
title (truncated to 80 chars) so the sessions list is human-readable.
"""

import logging
from textwrap import shorten

from sqlalchemy.orm import Session

from app.repositories.conversation_repository import ConversationRepository
from app.schemas.conversation import ConversationAskResponse
from app.services.ask_service import AskService

logger = logging.getLogger(__name__)

_MAX_HISTORY_CHARS = 1_200  # guard token budget for history prefix


class ConversationService:

    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = ConversationRepository(db)
        self.ask_service = AskService(db)

    # ------------------------------------------------------------------
    # Session management
    # ------------------------------------------------------------------

    def create_session(self, user_id: int) -> dict:
        session = self.repo.create_session(user_id=user_id)
        return self._session_to_dict(session, message_count=0)

    def get_session(self, session_id: int, user_id: int) -> dict | None:
        session = self.repo.get_session(session_id, user_id)
        if session is None:
            return None
        msgs = self.repo.get_recent_messages(session_id, limit=100)
        return {
            **self._session_to_dict(session, message_count=len(msgs)),
            "messages": [self._msg_to_dict(m) for m in msgs],
        }

    def list_sessions(self, user_id: int) -> list[dict]:
        sessions = self.repo.list_sessions(user_id)
        return [
            self._session_to_dict(s, self.repo.count_messages(s.id))
            for s in sessions
        ]

    def delete_session(self, session_id: int, user_id: int) -> bool:
        session = self.repo.get_session(session_id, user_id)
        if session is None:
            return False
        self.repo.delete_session(session)
        return True

    # ------------------------------------------------------------------
    # Multi-turn ask
    # ------------------------------------------------------------------

    def ask(
        self,
        session_id: int,
        question: str,
        user_id: int,
    ) -> ConversationAskResponse:
        session = self.repo.get_session(session_id, user_id)
        if session is None:
            raise ValueError(f"Session {session_id} not found for user {user_id}")

        # Auto-title the session from the first user question.
        if session.title is None:
            self.repo.update_session_title(session, shorten(question, width=80, placeholder="…"))

        # Build history prefix for the LLM.
        recent = self.repo.get_recent_messages(session_id)
        history_prefix = self._build_history_prefix(recent)

        # Enrich question with history so retrieval finds context-aware chunks.
        enriched_question = (
            f"{history_prefix}\n\nCurrent question: {question}"
            if history_prefix
            else question
        )

        # Persist the user turn immediately (before LLM so it's never lost).
        self.repo.add_message(session_id=session_id, role="user", content=question)

        # Core retrieval + synthesis pipeline.
        result = self.ask_service.ask(question=enriched_question, user_id=user_id)

        # Persist the assistant response.
        self.repo.add_message(
            session_id=session_id,
            role="assistant",
            content=result.get("answer", ""),
            citations=result.get("citations"),
        )

        logger.info(
            "CONV ASK session_id=%d user_id=%d history_turns=%d status=%s",
            session_id,
            user_id,
            len(recent),
            result.get("status", "ok"),
        )

        return ConversationAskResponse(
            session_id=session_id,
            question=question,
            answer=result.get("answer", ""),
            sources=result.get("sources", []),
            citations=result.get("citations", []),
            retrieval_only=result.get("retrieval_only", False),
            reranked=result.get("reranked", False),
            provider=result.get("provider"),
            status=result.get("status", "ok"),
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _build_history_prefix(messages: list) -> str:
        """
        Serialise recent messages into a compact history block.
        Older messages are dropped first if the total would exceed
        _MAX_HISTORY_CHARS, keeping the most recent turns.
        """
        if not messages:
            return ""
        lines = []
        total = 0
        for msg in reversed(messages):
            label = "User" if msg.role == "user" else "Assistant"
            line = f"{label}: {msg.content}"
            total += len(line)
            if total > _MAX_HISTORY_CHARS:
                break
            lines.append(line)
        if not lines:
            return ""
        lines.reverse()
        return "Previous conversation:\n" + "\n".join(lines)

    @staticmethod
    def _session_to_dict(session, message_count: int = 0) -> dict:
        return {
            "id": session.id,
            "title": session.title,
            "created_at": session.created_at,
            "updated_at": session.updated_at,
            "message_count": message_count,
        }

    @staticmethod
    def _msg_to_dict(msg) -> dict:
        return {
            "id": msg.id,
            "role": msg.role,
            "content": msg.content,
            "citations": msg.citations,
            "created_at": msg.created_at,
        }
