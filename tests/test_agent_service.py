"""
Unit tests for AgentService.

Gemini HTTP calls and DB interactions are fully mocked.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from app.services.agent_service import AgentService, MAX_ITERATIONS, _TOOLS


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_db():
    return MagicMock()


def _gemini_text_response(text: str) -> dict:
    return {
        "candidates": [
            {"content": {"parts": [{"text": text}]}}
        ]
    }


def _gemini_tool_call_response(tool_name: str, args: dict) -> dict:
    return {
        "candidates": [
            {
                "content": {
                    "parts": [{"functionCall": {"name": tool_name, "args": args}}]
                }
            }
        ]
    }


# ---------------------------------------------------------------------------
# Tool declarations
# ---------------------------------------------------------------------------

class TestToolDeclarations:
    def test_all_four_tools_declared(self):
        names = {t["name"] for t in _TOOLS}
        assert names == {"search_notes", "filter_by_category", "get_note_content", "list_categories"}

    def test_search_notes_requires_query(self):
        tool = next(t for t in _TOOLS if t["name"] == "search_notes")
        assert "query" in tool["parameters"]["required"]

    def test_get_note_content_requires_note_id(self):
        tool = next(t for t in _TOOLS if t["name"] == "get_note_content")
        assert "note_id" in tool["parameters"]["required"]


# ---------------------------------------------------------------------------
# AgentService._system_prompt
# ---------------------------------------------------------------------------

class TestSystemPrompt:
    def test_contains_strategy_guidance(self):
        prompt = AgentService._system_prompt("")
        assert "search_notes" in prompt
        assert "list_categories" in prompt

    def test_includes_history_when_provided(self):
        history = "Previous conversation:\nUser: Hello"
        prompt = AgentService._system_prompt(history)
        assert "Previous conversation:" in prompt


# ---------------------------------------------------------------------------
# AgentService._run_agent_loop — text-only first response
# ---------------------------------------------------------------------------

class TestRunAgentLoopDirectAnswer:
    def test_returns_answer_on_first_text_response(self):
        db = _make_db()
        with patch("app.services.agent_service.ChunkService"), \
             patch("app.services.agent_service.AskService"), \
             patch("app.services.agent_service.ConversationRepository"):
            svc = AgentService(db)
            svc._call_gemini = MagicMock(
                return_value=_gemini_text_response("Direct answer.")
            )
            result = svc._run_agent_loop("q", user_id=1, history_prefix="")

        assert result.answer == "Direct answer."
        assert result.iterations == 1
        assert result.tools_used == []
        assert result.status == "ok"


# ---------------------------------------------------------------------------
# AgentService._run_agent_loop — one tool call then answer
# ---------------------------------------------------------------------------

class TestRunAgentLoopWithToolCall:
    def test_executes_tool_and_returns_final_answer(self):
        db = _make_db()
        with patch("app.services.agent_service.ChunkService"), \
             patch("app.services.agent_service.AskService"), \
             patch("app.services.agent_service.ConversationRepository"):
            svc = AgentService(db)
            svc._call_gemini = MagicMock(side_effect=[
                _gemini_tool_call_response("list_categories", {}),
                _gemini_text_response("Based on your categories, the answer is X."),
            ])
            svc._execute_tool = MagicMock(return_value=('{"categories": ["Work"]}', []))

            result = svc._run_agent_loop("q", user_id=1, history_prefix="")

        assert "the answer is X" in result.answer
        assert "list_categories" in result.tools_used
        assert result.iterations == 2


# ---------------------------------------------------------------------------
# AgentService._run_agent_loop — Gemini failure falls back
# ---------------------------------------------------------------------------

class TestRunAgentLoopFallback:
    def test_falls_back_when_gemini_returns_none(self):
        db = _make_db()
        with patch("app.services.agent_service.ChunkService"), \
             patch("app.services.agent_service.AskService") as MockAsk, \
             patch("app.services.agent_service.ConversationRepository"):
            MockAsk.return_value.ask.return_value = {
                "answer": "fallback answer",
                "sources": [],
                "citations": [],
                "status": "ok",
            }
            svc = AgentService(db)
            svc._call_gemini = MagicMock(return_value=None)

            result = svc._run_agent_loop("q", user_id=1, history_prefix="")

        assert result.answer == "fallback answer"
        assert result.status == "fallback"

    def test_falls_back_after_max_iterations(self):
        db = _make_db()
        with patch("app.services.agent_service.ChunkService"), \
             patch("app.services.agent_service.AskService") as MockAsk, \
             patch("app.services.agent_service.ConversationRepository"):
            MockAsk.return_value.ask.return_value = {
                "answer": "fallback", "sources": [], "citations": [], "status": "ok"
            }
            svc = AgentService(db)
            svc._call_gemini = MagicMock(
                return_value=_gemini_tool_call_response("list_categories", {})
            )
            svc._execute_tool = MagicMock(return_value=('{"categories": []}', []))

            result = svc._run_agent_loop("q", user_id=1, history_prefix="")

        assert result.status == "fallback"
        assert svc._call_gemini.call_count == MAX_ITERATIONS


# ---------------------------------------------------------------------------
# AgentService.ask — no GEMINI_API_KEY falls back immediately
# ---------------------------------------------------------------------------

class TestAgentAskNoKey:
    def test_falls_back_when_no_api_key(self):
        db = _make_db()
        with patch("app.services.agent_service.ChunkService"), \
             patch("app.services.agent_service.AskService") as MockAsk, \
             patch("app.services.agent_service.ConversationRepository"), \
             patch("app.services.agent_service.settings") as mock_settings:
            mock_settings.GEMINI_API_KEY = None
            MockAsk.return_value.ask.return_value = {
                "answer": "no-key fallback",
                "sources": [],
                "citations": [],
                "status": "ok",
            }
            svc = AgentService(db)
            resp = svc.ask(question="q", user_id=1)

        assert resp.answer == "no-key fallback"
        assert resp.status == "fallback"


# ---------------------------------------------------------------------------
# AgentService — tool limit enforcement
# ---------------------------------------------------------------------------

class TestToolLimits:
    def test_search_notes_limit_capped_at_10(self):
        db = _make_db()
        with patch("app.services.agent_service.ChunkService") as MockChunk, \
             patch("app.services.agent_service.AskService"), \
             patch("app.services.agent_service.ConversationRepository"):
            MockChunk.return_value.retrieve_hybrid.return_value = []
            svc = AgentService(db)
            # Cap is enforced in _execute_tool before delegating to _tool_search_notes.
            svc._execute_tool("search_notes", {"query": "q", "limit": 999}, user_id=1)
            call_limit = MockChunk.return_value.retrieve_hybrid.call_args.kwargs["limit"]
            assert call_limit <= 10
