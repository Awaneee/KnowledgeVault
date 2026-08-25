"""
Agentic RAG service — Gemini function-calling agent over the knowledge base.

Architecture
------------
The agent runs a tool-calling loop (max MAX_ITERATIONS turns):

  1. Send the user question + available tools to Gemini.
  2. If Gemini issues a functionCall, execute the matching tool and feed the
     result back as a functionResponse.
  3. Repeat until Gemini returns a plain text answer or the iteration cap is hit.

Available tools
---------------
  search_notes(query, limit)         — hybrid semantic search
  filter_by_category(category, limit)— retrieve notes in a named category
  get_note_content(note_id)          — fetch full body of a specific note
  list_categories()                  — enumerate the user's categories

The agent can chain tools in a single request cycle.  A typical multi-hop
pattern: list_categories → filter_by_category → get_note_content → answer.

Fallback
--------
If Gemini is unavailable the service falls back to the standard AskService
single-shot pipeline so the endpoint never returns a 500.
"""

import json
import logging
import time
from dataclasses import dataclass, field

import requests

from app.core.config import settings
from app.models.notes import Note
from app.repositories.conversation_repository import ConversationRepository
from app.schemas.conversation import AgentAskResponse
from app.services.ask_service import AskService
from app.services.chunk_service import ChunkService

logger = logging.getLogger(__name__)

MAX_ITERATIONS = 5

# ---------------------------------------------------------------------------
# Tool declarations (Gemini function-calling schema)
# ---------------------------------------------------------------------------

_TOOLS = [
    {
        "name": "search_notes",
        "description": (
            "Semantic search over the user's knowledge base. "
            "Use when you need to find notes relevant to a topic or concept."
        ),
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "query": {
                    "type": "STRING",
                    "description": "Natural-language search query",
                },
                "limit": {
                    "type": "INTEGER",
                    "description": "Maximum number of results (1–10, default 5)",
                },
            },
            "required": ["query"],
        },
    },
    {
        "name": "filter_by_category",
        "description": (
            "Retrieve the most relevant notes inside a specific category. "
            "Use after list_categories to drill into a known category."
        ),
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "category": {
                    "type": "STRING",
                    "description": "Exact category name as returned by list_categories",
                },
                "limit": {
                    "type": "INTEGER",
                    "description": "Maximum number of notes (1–10, default 5)",
                },
            },
            "required": ["category"],
        },
    },
    {
        "name": "get_note_content",
        "description": (
            "Fetch the complete body text of a specific note by its ID. "
            "Use when a search result's snippet is insufficient."
        ),
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "note_id": {
                    "type": "INTEGER",
                    "description": "The note ID as returned in search results",
                },
            },
            "required": ["note_id"],
        },
    },
    {
        "name": "list_categories",
        "description": (
            "List all categories the user has organised their notes into. "
            "Use to understand available topic areas before filtering."
        ),
        "parameters": {
            "type": "OBJECT",
            "properties": {},
            "required": [],
        },
    },
]


# ---------------------------------------------------------------------------
# Agent result dataclass
# ---------------------------------------------------------------------------

@dataclass
class AgentResult:
    answer: str
    sources: list[str] = field(default_factory=list)
    citations: list[dict] = field(default_factory=list)
    tools_used: list[str] = field(default_factory=list)
    iterations: int = 0
    status: str = "ok"


# ---------------------------------------------------------------------------
# AgentService
# ---------------------------------------------------------------------------

class AgentService:

    def __init__(self, db) -> None:
        self.db = db
        self.chunk_service = ChunkService(db)
        self.ask_service = AskService(db)
        self.conv_repo = ConversationRepository(db)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def ask(
        self,
        question: str,
        user_id: int,
        session_id: int | None = None,
    ) -> AgentAskResponse:
        if not settings.GEMINI_API_KEY:
            logger.warning("AGENT falling back to AskService — GEMINI_API_KEY not configured")
            return self._fallback(question, user_id, session_id)

        # Load conversation history if a session is active.
        history_prefix = ""
        if session_id is not None:
            session = self.conv_repo.get_session(session_id, user_id)
            if session:
                recent = self.conv_repo.get_recent_messages(session_id)
                history_prefix = self._build_history_prefix(recent)

        result = self._run_agent_loop(
            question=question,
            user_id=user_id,
            history_prefix=history_prefix,
        )

        # Persist to conversation session if provided.
        if session_id is not None:
            session = self.conv_repo.get_session(session_id, user_id)
            if session:
                from textwrap import shorten
                if session.title is None:
                    self.conv_repo.update_session_title(
                        session, shorten(question, width=80, placeholder="…")
                    )
                self.conv_repo.add_message(session_id, "user", question)
                self.conv_repo.add_message(
                    session_id, "assistant", result.answer, result.citations or None
                )

        return AgentAskResponse(
            session_id=session_id or 0,
            question=question,
            answer=result.answer,
            sources=result.sources,
            citations=result.citations,
            tools_used=result.tools_used,
            iterations=result.iterations,
            status=result.status,
        )

    # ------------------------------------------------------------------
    # Core tool-calling loop
    # ------------------------------------------------------------------

    def _run_agent_loop(
        self,
        question: str,
        user_id: int,
        history_prefix: str,
    ) -> AgentResult:
        system_prompt = self._system_prompt(history_prefix)
        contents = [
            {"role": "user", "parts": [{"text": f"{system_prompt}\n\nQuestion: {question}"}]}
        ]

        tools_used: list[str] = []
        all_sources: list[str] = []

        for iteration in range(1, MAX_ITERATIONS + 1):
            logger.info("AGENT iteration=%d", iteration)
            response_data = self._call_gemini(contents)
            if response_data is None:
                logger.warning("AGENT Gemini call failed, falling back")
                break

            candidate = response_data.get("candidates", [{}])[0]
            parts = candidate.get("content", {}).get("parts", [])

            # Collect any tool calls in this turn.
            tool_calls = [p for p in parts if "functionCall" in p]
            text_parts = [p.get("text", "") for p in parts if "text" in p]

            if not tool_calls:
                # Gemini returned a final text answer.
                answer = " ".join(text_parts).strip()
                if answer:
                    return AgentResult(
                        answer=answer,
                        sources=list(dict.fromkeys(all_sources)),
                        tools_used=tools_used,
                        iterations=iteration,
                        status="ok",
                    )
                break

            # Append assistant message with function calls.
            contents.append({"role": "model", "parts": parts})

            # Execute each tool and collect results.
            tool_response_parts = []
            for tc in tool_calls:
                fn = tc["functionCall"]
                tool_name = fn["name"]
                args = fn.get("args", {})
                tools_used.append(tool_name)

                logger.info("AGENT tool=%s args=%s", tool_name, args)
                tool_result, sources = self._execute_tool(tool_name, args, user_id)
                all_sources.extend(sources)

                tool_response_parts.append({
                    "functionResponse": {
                        "name": tool_name,
                        "response": {"result": tool_result},
                    }
                })

            contents.append({"role": "user", "parts": tool_response_parts})

        # If we exhausted iterations or Gemini failed, fall back.
        logger.warning("AGENT exhausted iterations or Gemini unavailable — using AskService")
        fallback = self.ask_service.ask(question=question, user_id=user_id)
        return AgentResult(
            answer=fallback.get("answer", ""),
            sources=fallback.get("sources", []),
            citations=fallback.get("citations", []),
            tools_used=tools_used,
            iterations=MAX_ITERATIONS,
            status="fallback",
        )

    # ------------------------------------------------------------------
    # Tool implementations
    # ------------------------------------------------------------------

    def _execute_tool(
        self, tool_name: str, args: dict, user_id: int
    ) -> tuple[str, list[str]]:
        """Execute a tool and return (result_json_str, list_of_source_titles)."""
        try:
            if tool_name == "search_notes":
                return self._tool_search_notes(
                    query=args.get("query", ""),
                    limit=min(int(args.get("limit", 5)), 10),
                    user_id=user_id,
                )
            if tool_name == "filter_by_category":
                return self._tool_filter_by_category(
                    category=args.get("category", ""),
                    limit=min(int(args.get("limit", 5)), 10),
                    user_id=user_id,
                )
            if tool_name == "get_note_content":
                return self._tool_get_note_content(
                    note_id=int(args.get("note_id", 0)),
                    user_id=user_id,
                )
            if tool_name == "list_categories":
                return self._tool_list_categories(user_id=user_id)
            return json.dumps({"error": f"Unknown tool: {tool_name}"}), []
        except Exception as exc:
            logger.exception("AGENT tool=%s error: %s", tool_name, exc)
            return json.dumps({"error": str(exc)}), []

    def _tool_search_notes(
        self, query: str, limit: int, user_id: int
    ) -> tuple[str, list[str]]:
        chunks = self.chunk_service.retrieve_hybrid(
            query=query, user_id=user_id, limit=limit
        )
        results = [
            {
                "note_id": c["note_id"],
                "title": c["note_title"],
                "snippet": c["chunk_text"][:300],
                "score": round(c.get("score", 0.0), 3),
                "category": c.get("intent_category"),
            }
            for c in chunks
        ]
        sources = list(dict.fromkeys(c["note_title"] for c in chunks))
        return json.dumps({"results": results, "count": len(results)}), sources

    def _tool_filter_by_category(
        self, category: str, limit: int, user_id: int
    ) -> tuple[str, list[str]]:
        from app.models.notes import Note
        from app.models.note_intent_assignment import NoteIntentAssignment
        from app.models.intent_category import IntentCategory

        rows = (
            self.db.query(Note, IntentCategory.name)
            .join(NoteIntentAssignment, NoteIntentAssignment.note_id == Note.id)
            .join(IntentCategory, IntentCategory.id == NoteIntentAssignment.intent_category_id)
            .filter(
                Note.user_id == user_id,
                IntentCategory.name.ilike(f"%{category}%"),
            )
            .order_by(Note.updated_at.desc())
            .limit(limit)
            .all()
        )
        results = [
            {
                "note_id": note.id,
                "title": note.title,
                "snippet": (note.content or "")[:300],
                "category": cat_name,
            }
            for note, cat_name in rows
        ]
        sources = [r["title"] for r in results]
        return json.dumps({"results": results, "count": len(results)}), sources

    def _tool_get_note_content(
        self, note_id: int, user_id: int
    ) -> tuple[str, list[str]]:
        note = (
            self.db.query(Note)
            .filter(Note.id == note_id, Note.user_id == user_id)
            .first()
        )
        if note is None:
            return json.dumps({"error": "Note not found"}), []
        return json.dumps({"note_id": note.id, "title": note.title, "content": note.content or ""}), [note.title]

    def _tool_list_categories(self, user_id: int) -> tuple[str, list[str]]:
        from app.models.intent_category import IntentCategory

        cats = (
            self.db.query(IntentCategory.name)
            .filter(IntentCategory.user_id == user_id)
            .order_by(IntentCategory.name)
            .all()
        )
        names = [c[0] for c in cats]
        return json.dumps({"categories": names, "count": len(names)}), []

    # ------------------------------------------------------------------
    # Gemini function-calling API call
    # ------------------------------------------------------------------

    def _call_gemini(self, contents: list[dict]) -> dict | None:
        url = (
            f"{settings.GEMINI_API_BASE}/models/{settings.GEMINI_ANSWER_MODEL}"
            f":generateContent?key={settings.GEMINI_API_KEY}"
        )
        payload = {
            "contents": contents,
            "tools": [{"functionDeclarations": _TOOLS}],
            "generationConfig": {"temperature": 0.1},
        }
        try:
            resp = requests.post(url, json=payload, timeout=settings.LLM_TIMEOUT_SECONDS)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as exc:
            logger.warning("AGENT Gemini API error: %s", exc)
            return None

    # ------------------------------------------------------------------
    # Fallback to standard AskService
    # ------------------------------------------------------------------

    def _fallback(
        self, question: str, user_id: int, session_id: int | None
    ) -> AgentAskResponse:
        result = self.ask_service.ask(question=question, user_id=user_id)
        return AgentAskResponse(
            session_id=session_id or 0,
            question=question,
            answer=result.get("answer", ""),
            sources=result.get("sources", []),
            citations=result.get("citations", []),
            tools_used=[],
            iterations=0,
            status="fallback",
        )

    # ------------------------------------------------------------------
    # History helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _build_history_prefix(messages: list) -> str:
        lines = []
        total = 0
        for msg in reversed(messages[-10:]):
            label = "User" if msg.role == "user" else "Assistant"
            line = f"{label}: {msg.content}"
            total += len(line)
            if total > 1_200:
                break
            lines.append(line)
        if not lines:
            return ""
        lines.reverse()
        return "Previous conversation:\n" + "\n".join(lines)

    @staticmethod
    def _system_prompt(history_prefix: str) -> str:
        base = (
            "You are an intelligent assistant with access to the user's personal knowledge base. "
            "Use the provided tools to search, filter, and retrieve notes before answering. "
            "Always ground your answer in retrieved content. "
            "Cite note titles when you reference them. "
            "If the tools return no useful results, say so honestly.\n\n"
            "Strategy: start broad (search_notes or list_categories), then drill down "
            "(filter_by_category, get_note_content) if needed."
        )
        if history_prefix:
            return f"{base}\n\n{history_prefix}"
        return base
