"""
Streaming ask — citations over SSE, and the /ask rate-limit key.

Pure Python: no database, no network, no LLM call.
"""
from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

from fastapi import Request

from app.api.sse import sse_stream
from app.core.limiter import user_or_ip_key
from app.core.security import create_access_token
from app.schemas.ask import Citation
from app.services.ask_service import AskService, StreamCitations


def _chunk(note_id: int) -> dict:
    return {
        "note_id": note_id,
        "note_title": f"Note {note_id}",
        "chunk_id": note_id * 10,
        "chunk_text": f"Content of note {note_id}. " * 6,
        "chunk_index": 0,
        "score": 0.8,
        "semantic_score": 0.8,
        "intent_score": 0.0,
        "source": "semantic",
        "intent_category": None,
    }


def _service() -> AskService:
    svc = AskService.__new__(AskService)
    svc.chunk_service = MagicMock()
    svc.chunk_service.retrieve_hybrid.return_value = [_chunk(1), _chunk(2)]
    return svc


def _parse_frames(frames: list[str]) -> list[tuple[str | None, str]]:
    """[(event, data_line)] for each SSE frame."""
    out = []
    for frame in frames:
        event = None
        data = ""
        for line in frame.strip().split("\n"):
            if line.startswith("event: "):
                event = line[7:]
            elif line.startswith("data: "):
                data = line[6:]
        out.append((event, data))
    return out


# ---------------------------------------------------------------------------
# stream_ask
# ---------------------------------------------------------------------------

@patch("app.services.ask_service.LLMService")
@patch("app.services.ask_service.RerankingService")
@patch("app.services.ask_service.settings")
class TestStreamAskCitations:

    def _run(self, mock_settings, mock_reranker, mock_llm, tokens):
        mock_settings.RERANKING_ENABLED = False
        mock_settings.RETRIEVAL_MIN_SCORE = 0.0
        mock_reranker.rerank.side_effect = lambda **kw: MagicMock(
            candidates=kw["candidates"], reranked=False
        )
        mock_llm.generate_stream.return_value = iter(tokens)
        return list(_service().stream_ask("q", user_id=1))

    def test_yields_citations_after_last_token(self, s, r, l):
        items = self._run(s, r, l, ["Redis is fast ", "[1", "] and ", "durable [2]."])
        assert items[:4] == ["Redis is fast ", "[1", "] and ", "durable [2]."]
        last = items[-1]
        assert isinstance(last, StreamCitations)
        assert [c.ref for c in last.citations] == [1, 2]
        assert last.citations[0].note_title == "Note 1"

    def test_marker_split_across_tokens_is_resolved(self, s, r, l):
        items = self._run(s, r, l, ["see [", "1", "]"])
        assert isinstance(items[-1], StreamCitations)
        assert items[-1].citations[0].ref == 1

    def test_out_of_range_marker_is_ignored(self, s, r, l):
        items = self._run(s, r, l, ["only two notes [9]"])
        assert items == ["only two notes [9]"]

    def test_no_markers_means_no_citation_item(self, s, r, l):
        items = self._run(s, r, l, ["plain ", "answer"])
        assert items == ["plain ", "answer"]

    def test_degraded_message_carries_no_citations(self, s, r, l):
        from app.services.llm_service import AllProvidersExhausted

        def boom(**_):
            raise AllProvidersExhausted("all down")
            yield  # pragma: no cover

        s.RERANKING_ENABLED = False
        s.RETRIEVAL_MIN_SCORE = 0.0
        r.rerank.side_effect = lambda **kw: MagicMock(
            candidates=kw["candidates"], reranked=False
        )
        l.generate_stream.side_effect = boom
        items = list(_service().stream_ask("q", user_id=1))
        assert len(items) == 1 and isinstance(items[0], str)
        assert "temporarily unavailable" in items[0]


# ---------------------------------------------------------------------------
# sse_stream framing
# ---------------------------------------------------------------------------

class TestSseStream:

    def test_tokens_are_json_encoded_and_done_terminates(self):
        frames = list(sse_stream(iter(["a\n", " b"])))
        parsed = _parse_frames(frames)
        assert parsed[0] == (None, json.dumps("a\n"))
        assert parsed[1] == (None, json.dumps(" b"))
        assert parsed[-1] == (None, "[DONE]")

    def test_citations_frame_has_event_name_and_json_array(self):
        cite = Citation(ref=1, note_id=7, note_title="N", chunk_id=None, snippet="s")
        frames = list(sse_stream(iter(["x [1]", StreamCitations([cite])])))
        parsed = _parse_frames(frames)
        assert parsed[1][0] == "citations"
        payload = json.loads(parsed[1][1])
        assert payload == [
            {"ref": 1, "note_id": 7, "note_title": "N", "chunk_id": None, "snippet": "s"}
        ]
        assert parsed[-1] == (None, "[DONE]")

    def test_mid_stream_error_emits_error_event_then_done(self):
        def gen():
            yield "partial"
            raise RuntimeError("provider blew up")

        parsed = _parse_frames(list(sse_stream(gen())))
        assert parsed[0] == (None, json.dumps("partial"))
        assert parsed[1][0] == "error"
        assert parsed[-1] == (None, "[DONE]")

    def test_empty_tokens_are_skipped(self):
        parsed = _parse_frames(list(sse_stream(iter(["", "hi"]))))
        assert [d for _, d in parsed] == [json.dumps("hi"), "[DONE]"]


# ---------------------------------------------------------------------------
# rate-limit key
# ---------------------------------------------------------------------------

def _request(headers: dict[str, str], client=("203.0.113.9", 1234)) -> Request:
    scope = {
        "type": "http",
        "headers": [(k.lower().encode(), v.encode()) for k, v in headers.items()],
        "client": client,
    }
    return Request(scope)


class TestUserOrIpKey:

    def test_valid_token_keys_by_user(self):
        token = create_access_token({"sub": "42"})
        assert user_or_ip_key(_request({"Authorization": f"Bearer {token}"})) == "user:42"

    def test_two_users_same_ip_get_different_keys(self):
        a = create_access_token({"sub": "1"})
        b = create_access_token({"sub": "2"})
        assert user_or_ip_key(_request({"Authorization": f"Bearer {a}"})) != \
            user_or_ip_key(_request({"Authorization": f"Bearer {b}"}))

    def test_invalid_token_falls_back_to_ip(self):
        assert user_or_ip_key(_request({"Authorization": "Bearer garbage"})) == "203.0.113.9"

    def test_missing_header_falls_back_to_ip(self):
        assert user_or_ip_key(_request({})) == "203.0.113.9"


# ---------------------------------------------------------------------------
# /ask rate limit — end to end through the real router
# ---------------------------------------------------------------------------

class TestAskRateLimit:

    def _client(self):
        from fastapi import FastAPI
        from fastapi.testclient import TestClient
        from slowapi import _rate_limit_exceeded_handler
        from slowapi.errors import RateLimitExceeded
        from slowapi.middleware import SlowAPIMiddleware

        from app.api.dependencies.auth import get_current_user
        from app.api.routes import ask as ask_routes
        from app.core.limiter import limiter
        from app.database.session import get_db

        limiter.reset()
        app = FastAPI()
        app.state.limiter = limiter
        app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
        app.add_middleware(SlowAPIMiddleware)
        app.include_router(ask_routes.router)
        app.dependency_overrides[get_db] = lambda: MagicMock()
        app.dependency_overrides[get_current_user] = lambda: MagicMock(id=1)
        return TestClient(app)

    def test_limit_is_shared_across_ask_and_stream_and_returns_429(self):
        from app.core.config import settings

        limit = int(settings.ASK_RATE_LIMIT.split("/")[0])
        client = self._client()
        token = create_access_token({"sub": "1"})
        headers = {"Authorization": f"Bearer {token}"}

        with patch("app.api.routes.ask.AskService") as svc:
            svc.return_value.ask.return_value = {
                "question": "q", "answer": "a", "sources": [],
            }
            svc.return_value.stream_ask.return_value = iter([])

            codes = []
            for i in range(limit + 1):
                path = "/ask/" if i % 2 == 0 else "/ask/stream"
                codes.append(client.post(path, json={"question": "q"}, headers=headers).status_code)

        assert codes[:limit] == [200] * limit
        assert codes[limit] == 429

    def test_other_user_is_not_throttled_by_first_users_traffic(self):
        from app.core.config import settings

        limit = int(settings.ASK_RATE_LIMIT.split("/")[0])
        client = self._client()
        h1 = {"Authorization": f"Bearer {create_access_token({'sub': '1'})}"}
        h2 = {"Authorization": f"Bearer {create_access_token({'sub': '2'})}"}

        with patch("app.api.routes.ask.AskService") as svc:
            svc.return_value.ask.return_value = {"question": "q", "answer": "a", "sources": []}
            for _ in range(limit + 1):
                client.post("/ask/", json={"question": "q"}, headers=h1)
            assert client.post("/ask/", json={"question": "q"}, headers=h1).status_code == 429
            assert client.post("/ask/", json={"question": "q"}, headers=h2).status_code == 200
