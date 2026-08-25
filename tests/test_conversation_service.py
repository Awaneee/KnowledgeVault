"""
Unit tests for ConversationService and ConversationRepository.

All DB and AskService calls are mocked — no real database required.
"""

from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import MagicMock, patch, call

import pytest

from app.services.conversation_service import ConversationService, _MAX_HISTORY_CHARS


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def _make_db():
    return MagicMock()


def _make_session(id_: int = 1, user_id: int = 42, title: str | None = None):
    s = MagicMock()
    s.id = id_
    s.user_id = user_id
    s.title = title
    s.created_at = datetime(2026, 8, 25, tzinfo=timezone.utc)
    s.updated_at = datetime(2026, 8, 25, tzinfo=timezone.utc)
    return s


def _make_message(id_: int, role: str, content: str):
    m = MagicMock()
    m.id = id_
    m.role = role
    m.content = content
    m.citations = None
    m.created_at = datetime(2026, 8, 25, tzinfo=timezone.utc)
    return m


# ---------------------------------------------------------------------------
# _build_history_prefix
# ---------------------------------------------------------------------------

class TestBuildHistoryPrefix:
    def test_empty_messages_returns_empty(self):
        assert ConversationService._build_history_prefix([]) == ""

    def test_single_user_message(self):
        msgs = [_make_message(1, "user", "Hello")]
        result = ConversationService._build_history_prefix(msgs)
        assert "Previous conversation:" in result
        assert "User: Hello" in result

    def test_user_and_assistant(self):
        msgs = [
            _make_message(1, "user", "What is X?"),
            _make_message(2, "assistant", "X is Y."),
        ]
        result = ConversationService._build_history_prefix(msgs)
        assert "User: What is X?" in result
        assert "Assistant: X is Y." in result

    def test_respects_char_limit(self):
        long_content = "a" * (_MAX_HISTORY_CHARS + 500)
        msgs = [_make_message(1, "user", long_content)]
        result = ConversationService._build_history_prefix(msgs)
        assert len(result) <= _MAX_HISTORY_CHARS + 50  # small overhead for label

    def test_keeps_most_recent_when_truncating(self):
        old = _make_message(1, "user", "very old question " + "x" * 600)
        recent = _make_message(2, "user", "recent question")
        # Put old first, recent last — the helper reverses to find most recent.
        msgs = [old, recent]
        result = ConversationService._build_history_prefix(msgs)
        assert "recent question" in result


# ---------------------------------------------------------------------------
# ConversationService.create_session
# ---------------------------------------------------------------------------

class TestCreateSession:
    def test_returns_session_dict(self):
        db = _make_db()
        with patch("app.services.conversation_service.ConversationRepository") as MockRepo, \
             patch("app.services.conversation_service.AskService"):
            mock_repo = MockRepo.return_value
            session = _make_session()
            mock_repo.create_session.return_value = session

            svc = ConversationService(db)
            result = svc.create_session(user_id=42)

        assert result["id"] == 1
        assert result["message_count"] == 0
        mock_repo.create_session.assert_called_once_with(user_id=42)


# ---------------------------------------------------------------------------
# ConversationService.get_session
# ---------------------------------------------------------------------------

class TestGetSession:
    def test_returns_none_when_not_found(self):
        db = _make_db()
        with patch("app.services.conversation_service.ConversationRepository") as MockRepo, \
             patch("app.services.conversation_service.AskService"):
            MockRepo.return_value.get_session.return_value = None
            svc = ConversationService(db)
            assert svc.get_session(session_id=99, user_id=1) is None

    def test_returns_session_with_messages(self):
        db = _make_db()
        with patch("app.services.conversation_service.ConversationRepository") as MockRepo, \
             patch("app.services.conversation_service.AskService"):
            mock_repo = MockRepo.return_value
            session = _make_session()
            msgs = [_make_message(1, "user", "q"), _make_message(2, "assistant", "a")]
            mock_repo.get_session.return_value = session
            mock_repo.get_recent_messages.return_value = msgs

            svc = ConversationService(db)
            result = svc.get_session(session_id=1, user_id=42)

        assert result["id"] == 1
        assert result["message_count"] == 2
        assert len(result["messages"]) == 2


# ---------------------------------------------------------------------------
# ConversationService.delete_session
# ---------------------------------------------------------------------------

class TestDeleteSession:
    def test_returns_false_when_not_found(self):
        db = _make_db()
        with patch("app.services.conversation_service.ConversationRepository") as MockRepo, \
             patch("app.services.conversation_service.AskService"):
            MockRepo.return_value.get_session.return_value = None
            svc = ConversationService(db)
            assert svc.delete_session(session_id=99, user_id=1) is False

    def test_returns_true_and_calls_delete(self):
        db = _make_db()
        with patch("app.services.conversation_service.ConversationRepository") as MockRepo, \
             patch("app.services.conversation_service.AskService"):
            mock_repo = MockRepo.return_value
            session = _make_session()
            mock_repo.get_session.return_value = session

            svc = ConversationService(db)
            result = svc.delete_session(session_id=1, user_id=42)

        assert result is True
        mock_repo.delete_session.assert_called_once_with(session)


# ---------------------------------------------------------------------------
# ConversationService.ask
# ---------------------------------------------------------------------------

class TestConversationAsk:
    def _make_ask_result(self) -> dict:
        return {
            "answer": "The answer is 42.",
            "sources": ["Note A"],
            "citations": [{"ref": 1, "note_title": "Note A"}],
            "retrieval_only": False,
            "reranked": False,
            "provider": "gemini",
            "status": "ok",
        }

    def test_raises_when_session_not_found(self):
        db = _make_db()
        with patch("app.services.conversation_service.ConversationRepository") as MockRepo, \
             patch("app.services.conversation_service.AskService"):
            MockRepo.return_value.get_session.return_value = None
            svc = ConversationService(db)
            with pytest.raises(ValueError, match="Session"):
                svc.ask(session_id=99, question="q", user_id=1)

    def test_persists_user_and_assistant_messages(self):
        db = _make_db()
        with patch("app.services.conversation_service.ConversationRepository") as MockRepo, \
             patch("app.services.conversation_service.AskService") as MockAsk:
            mock_repo = MockRepo.return_value
            session = _make_session()
            mock_repo.get_session.return_value = session
            mock_repo.get_recent_messages.return_value = []
            MockAsk.return_value.ask.return_value = self._make_ask_result()

            svc = ConversationService(db)
            svc.ask(session_id=1, question="What is 6x7?", user_id=42)

        add_calls = mock_repo.add_message.call_args_list
        assert add_calls[0] == call(session_id=1, role="user", content="What is 6x7?")
        assert add_calls[1].kwargs["role"] == "assistant"
        assert add_calls[1].kwargs["content"] == "The answer is 42."

    def test_auto_titles_untitled_session(self):
        db = _make_db()
        with patch("app.services.conversation_service.ConversationRepository") as MockRepo, \
             patch("app.services.conversation_service.AskService") as MockAsk:
            mock_repo = MockRepo.return_value
            session = _make_session(title=None)
            mock_repo.get_session.return_value = session
            mock_repo.get_recent_messages.return_value = []
            MockAsk.return_value.ask.return_value = self._make_ask_result()

            svc = ConversationService(db)
            svc.ask(session_id=1, question="First question", user_id=42)

        mock_repo.update_session_title.assert_called_once()
        title_arg = mock_repo.update_session_title.call_args[0][1]
        assert "First question" in title_arg

    def test_does_not_retitle_already_titled_session(self):
        db = _make_db()
        with patch("app.services.conversation_service.ConversationRepository") as MockRepo, \
             patch("app.services.conversation_service.AskService") as MockAsk:
            mock_repo = MockRepo.return_value
            session = _make_session(title="Existing Title")
            mock_repo.get_session.return_value = session
            mock_repo.get_recent_messages.return_value = []
            MockAsk.return_value.ask.return_value = self._make_ask_result()

            svc = ConversationService(db)
            svc.ask(session_id=1, question="Another question", user_id=42)

        mock_repo.update_session_title.assert_not_called()

    def test_history_prefix_is_prepended_to_question(self):
        db = _make_db()
        with patch("app.services.conversation_service.ConversationRepository") as MockRepo, \
             patch("app.services.conversation_service.AskService") as MockAsk:
            mock_repo = MockRepo.return_value
            session = _make_session(title="Existing")
            mock_repo.get_session.return_value = session
            mock_repo.get_recent_messages.return_value = [
                _make_message(1, "user", "Tell me about Python."),
            ]
            MockAsk.return_value.ask.return_value = self._make_ask_result()

            svc = ConversationService(db)
            svc.ask(session_id=1, question="What about its typing?", user_id=42)

        enriched_question = MockAsk.return_value.ask.call_args.kwargs["question"]
        assert "Previous conversation:" in enriched_question
        assert "Tell me about Python." in enriched_question
        assert "What about its typing?" in enriched_question

    def test_returns_correct_response_shape(self):
        db = _make_db()
        with patch("app.services.conversation_service.ConversationRepository") as MockRepo, \
             patch("app.services.conversation_service.AskService") as MockAsk:
            mock_repo = MockRepo.return_value
            session = _make_session(title="T")
            mock_repo.get_session.return_value = session
            mock_repo.get_recent_messages.return_value = []
            MockAsk.return_value.ask.return_value = self._make_ask_result()

            svc = ConversationService(db)
            resp = svc.ask(session_id=1, question="q", user_id=42)

        assert resp.session_id == 1
        assert resp.answer == "The answer is 42."
        assert resp.sources == ["Note A"]
        assert resp.status == "ok"
