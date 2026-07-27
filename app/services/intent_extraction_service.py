"""
Intent extraction service.

Responsibilities:
  - Build the LLM prompt and call LLMService.extract_intent() (structured JSON).
  - Validate and sanitize every LLM field before it touches any other layer.
  - Provide a fast keyword-only fallback for query-time classification.
  - Never make category-naming decisions — that belongs to IntentCategoryService.

Validation contract
-------------------
No field is passed downstream unless it has been sanitised by one of the
_clean_* helpers below.  Any value that would overflow a database column,
contain invisible Unicode, or is a structured type (dict/list) is either
repaired or discarded.  All repairs are logged at WARNING level.
"""

import json
import logging
import re
import unicodedata
from datetime import date
from datetime import datetime
from datetime import timedelta

from app.services.llm_service import LLMService


logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Column length limits (must match SQLAlchemy models exactly)
# ---------------------------------------------------------------------------
_LEN_INTENT_TYPE = 50
_LEN_ACTION = 80
_LEN_ACTOR = 120
_LEN_OBJECT = 255
_LEN_TEMPORAL = 120
_LEN_URGENCY = 30
_LEN_TOPIC = 120
_LEN_SUBTOPIC = 120

VALID_INTENT_TYPES = {
    "communication",
    "todo",
    "study",
    "reminder",
    "idea",
    "reference",
    "question",
    "event",
    "general",
}

# Common LLM synonyms that should map to canonical intent types.
INTENT_TYPE_SYNONYMS: dict[str, str] = {
    "task": "todo",
    "tasks": "todo",
    "action": "todo",
    "learn": "study",
    "learning": "study",
    "knowledge": "reference",
    "info": "reference",
    "information": "reference",
    "note": "general",
    "notes": "general",
    "thought": "idea",
    "thoughts": "idea",
    "brainstorm": "idea",
    "meeting": "event",
    "appointment": "reminder",
    "message": "communication",
    "email": "communication",
}

VALID_URGENCY = {"low", "medium", "high"}


class IntentExtractionService:
    PROMPT_VERSION = "intent-v2"

    TECH_MAP = {
        "redis": "Redis",
        "postgresql": "PostgreSQL",
        "postgres": "PostgreSQL",
        "docker": "Docker",
        "kafka": "Kafka",
        "kubernetes": "Kubernetes",
        "k8s": "Kubernetes",
        "mongodb": "MongoDB",
        "sqlite": "SQLite",
        "nginx": "Nginx",
        "react": "React",
        "flutter": "Flutter",
        "django": "Django",
        "flask": "Flask",
        "fastapi": "FastAPI",
        "pytorch": "PyTorch",
        "tensorflow": "TensorFlow",
        "langchain": "LangChain",
        "github": "GitHub",
        "gitlab": "GitLab",
        "aws": "AWS",
        "gcp": "GCP",
        "azure": "Azure",
        "python": "Python",
        "javascript": "JavaScript",
        "typescript": "TypeScript",
        "go": "Go",
        "rust": "Rust",
        "java": "Java",
        "cpp": "C++",
        "html": "HTML",
        "css": "CSS",
        "sql": "SQL",
        "nosql": "NoSQL"
    }

    COMMUNICATION_ACTIONS = {
        "tell", "inform", "discuss", "ask", "message",
        "call", "email", "share", "meet",
    }

    TODO_ACTIONS = {
        "do", "finish", "prepare", "submit", "buy", "eat", "take",
        "revise", "complete", "practice", "study",
    }

    # --- Query-time fast classifier (no LLM) ---------------------------
    QUERY_COMMUNICATION_KEYWORDS = {
        "tell", "inform", "discuss", "ask", "message",
        "call", "email", "share", "meet", "talk",
    }
    QUERY_TODO_KEYWORDS = {
        "todo", "to-do", "task", "tasks", "pending",
        "finish", "complete", "submit", "buy", "pay",
    }
    QUERY_STUDY_KEYWORDS = {
        "study", "studies", "learn", "learning",
        "revise", "revision", "practice",
    }
    QUERY_IDEA_KEYWORDS = {
        "idea", "ideas", "startup", "concept", "concepts", "brainstorm",
    }
    QUERY_REFERENCE_KEYWORDS = {
        "reference", "references", "docs", "documentation",
    }
    QUERY_EVENT_KEYWORDS = {
        "event", "events", "meeting", "meetings", "scheduled", "schedule",
    }
    QUERY_REMINDER_KEYWORDS = {
        "remind", "reminder", "reminders", "appointment", "appointments",
    }
    QUERY_QUESTION_KEYWORDS = {
        "what", "how", "why", "when", "where", "who", "which",
    }

    # Priority order: first match wins.
    QUERY_INTENT_KEYWORD_GROUPS = (
        ("communication", QUERY_COMMUNICATION_KEYWORDS),
        ("reminder", QUERY_REMINDER_KEYWORDS),
        ("study", QUERY_STUDY_KEYWORDS),
        ("idea", QUERY_IDEA_KEYWORDS),
        ("reference", QUERY_REFERENCE_KEYWORDS),
        ("event", QUERY_EVENT_KEYWORDS),
        ("todo", QUERY_TODO_KEYWORDS),
    )

    # Stopwords stripped before scanning for actor/topic tokens.
    QUERY_STOPWORDS = {
        "i", "me", "my", "what", "should", "do", "need", "to", "the",
        "a", "an", "about", "for", "with", "on", "in", "at", "is", "are", "of",
        "and", "or", "but", "by", "from",
        "things", "thing", "tell", "inform", "discuss", "ask", "message",
        "call", "email", "share", "meet", "talk", "todo", "to-do", "task",
        "tasks", "pending", "finish", "complete", "submit", "buy", "pay",
        "study", "studies", "learn", "learning", "revise", "revision",
        "practice", "idea", "ideas", "startup", "concept", "concepts",
        "brainstorm", "reference", "references", "docs", "documentation",
        "notes", "note", "event", "events", "meeting", "meetings",
        "scheduled", "schedule", "remind", "reminder", "reminders",
        "appointment", "appointments",
    }

    # Generic single-token words that are almost never real actor names.
    _ACTOR_GENERIC_WORDS = {
        "team", "project", "work", "group", "class", "course",
        "everyone", "all", "us", "them", "people", "person",
        "someone", "anyone", "no", "yes", "sir", "ma'am",
        "management", "department", "company", "org", "office",
        "staff", "admin", "system", "service", "server", "client",
        "user", "users", "manager", "lead", "head", "hr",
        "internship", "interview", "assignment", "deadline", "report",
        "presentation", "capstone", "semester", "college", "university",
        "professor", "faculty", "lab", "exam", "test", "quiz",
        "module", "chapter", "topic", "subject", "problem", "solution",
        "update", "status", "feedback", "review", "discussion",
        "issue", "ticket", "request", "feature", "bug", "fix",
        "important", "urgent", "asap", "later", "soon", "quick",
        "new", "old", "big", "small", "good", "bad", "best", "next",
        "first", "last", "latest", "current", "upcoming", "recent",
        "other", "another", "same", "different", "possible", "available",
    }

    GENERIC_OBJECT_WORDS = {
        "general", "study", "todo", "to do", "task", "tasks", "note",
        "notes", "thing", "things", "item", "items", "object", "topic",
        "work", "personal",
    }

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def extract(self, title: str, content: str | None) -> dict:
        """
        Full intent extraction for a note being indexed.
        Tries LLM first; falls back to rule-based classifier on any failure.
        """
        text = self._build_text(title, content)

        if not text or not text.strip():
            logger.warning("INTENT EXTRACTION: empty text, using rule fallback")
            return self._extract_with_rules("Untitled")

        # Guard against extremely long notes overwhelming the LLM context.
        text_for_llm = text[:4000] if len(text) > 4000 else text

        logger.info(
            "\n%s\nINTENT EXTRACTION INPUT (%.0f chars)\n%s\n%.200s",
            "=" * 60,
            len(text_for_llm),
            "=" * 60,
            text_for_llm,
        )

        try:
            raw = self._extract_with_llm(text_for_llm)
            result = self._normalize(raw, text_for_llm)
            logger.info(
                "INTENT EXTRACTED provider=%s intent=%s actor=%s topic=%s object=%s confidence=%.2f",
                raw.get("_provider", "unknown"),
                result["intent_type"],
                result.get("actor"),
                result.get("topic"),
                result.get("object"),
                result["confidence"],
            )
            return result
        except Exception as exc:
            logger.exception(
                "INTENT EXTRACTION LLM FAILED — falling back to rules. error=%s", exc
            )
            rule_result = self._extract_with_rules(text_for_llm)

            from app.core.config import settings
            if settings.OLLAMA_ENABLED:
                try:
                    logger.info("Ollama is enabled, attempting Ollama intent extraction fallback")
                    from app.services.llm_providers import OllamaProvider
                    from app.services.llm_service import _try_repair_json, is_valid_intent_json
                    provider = OllamaProvider()
                    prompt = self._build_prompt(text_for_llm)
                    llm_result = provider.extract_intent(prompt)
                    if is_valid_intent_json(llm_result.text):
                        repaired = _try_repair_json(llm_result.text)
                        raw_ollama = json.loads(repaired)
                        raw_ollama["_provider"] = "ollama"
                        ollama_result = self._normalize(raw_ollama, text_for_llm)
                        logger.info("Ollama intent extraction succeeded")
                        return ollama_result
                except Exception as ollama_exc:
                    logger.warning("Ollama intent extraction fallback failed: %s", ollama_exc)

            return rule_result

    def extract_query_intent(self, query: str) -> dict:
        """Full LLM-backed intent classification for a retrieval query."""
        try:
            raw = self._extract_with_llm(query, is_query=True)
            return self._normalize(raw, query)
        except Exception:
            rule_result = self._extract_with_rules(query)

            from app.core.config import settings
            if settings.OLLAMA_ENABLED:
                try:
                    logger.info("Ollama is enabled, attempting Ollama query intent extraction fallback")
                    from app.services.llm_providers import OllamaProvider
                    from app.services.llm_service import _try_repair_json, is_valid_intent_json
                    provider = OllamaProvider()
                    prompt = self._build_prompt(query, is_query=True)
                    llm_result = provider.extract_intent(prompt)
                    if is_valid_intent_json(llm_result.text):
                        repaired = _try_repair_json(llm_result.text)
                        raw_ollama = json.loads(repaired)
                        raw_ollama["_provider"] = "ollama"
                        ollama_result = self._normalize(raw_ollama, query)
                        logger.info("Ollama query intent extraction succeeded")
                        return ollama_result
                except Exception as ollama_exc:
                    logger.warning("Ollama query intent extraction fallback failed: %s", ollama_exc)

            return rule_result

    def extract_query_intent_fast(self, query: str) -> dict:
        """
        Lightweight keyword-based classifier for Ask-time queries.
        No LLM — runs in microseconds.  Used by IntentCategoryService so
        retrieval never blocks on an LLM call.

        Extracts: intent_type, action, actor, topic (pseudo), object (pseudo).
        """
        logger.info("FAST CLASSIFIER activated query=%.80s", query)

        lowered = query.lower().strip()
        words = re.findall(r"[a-z0-9']+", lowered)
        word_set = set(words)

        intent_type = "general"
        confidence = 0.5

        for candidate_type, keywords in self.QUERY_INTENT_KEYWORD_GROUPS:
            if word_set & keywords:
                intent_type = candidate_type
                confidence = 0.65
                break

        if intent_type == "general" and word_set & self.QUERY_QUESTION_KEYWORDS:
            intent_type = "question"
            confidence = 0.55

        # Actor extraction — only for communication intents.
        actor = None
        if intent_type == "communication":
            actor = self._find_query_actor(words)
            if actor:
                confidence = 0.72

        # Topic extraction — pull meaningful content words for vector
        # signatures, regardless of intent type.
        topic = self._extract_pseudo_topic(
            words=words,
            intent_type=intent_type,
            actor=actor,
        )

        # object = same as topic for backward-compat with callers that
        # still use intent["object"] for retrieval.
        pseudo_object = topic

        action = (
            next(iter(word_set & self.QUERY_COMMUNICATION_KEYWORDS), None)
            if intent_type == "communication"
            else None
        )

        result = {
            "intent_type": intent_type,
            "action": action,
            "actor": actor,
            "topic": topic,
            "subtopic": None,
            "object": pseudo_object,
            "due_date": None,
            "temporal_text": None,
            "urgency": "medium",
            "category_hint": None,
            "confidence": confidence,
            "reasoning_summary": "Fast keyword-based query classification.",
            "raw_llm_json": None,
            "model_name": "heuristic-fast",
            "prompt_version": self.PROMPT_VERSION,
            "source_text": query,
        }

        logger.info(
            "FAST CLASSIFIER RESULT intent=%s actor=%s topic=%s confidence=%.2f",
            intent_type,
            actor,
            topic,
            confidence,
        )

        return result

    # ------------------------------------------------------------------
    # LLM extraction
    # ------------------------------------------------------------------

    def _build_text(self, title: str, content: str | None) -> str:
        title = (title or "").strip() or "Untitled"
        if content and content.strip():
            return f"{title}\n{content.strip()}"
        return title

    def _extract_with_llm(self, text: str, is_query: bool = False) -> dict:
        prompt = self._build_prompt(text, is_query=is_query)

        llm_result = LLMService.extract_intent(prompt)

        if llm_result.fallback_events:
            logger.warning(
                "INTENT LLM FALLBACK events=%s", llm_result.fallback_events
            )

        logger.debug("LLM RAW RESPONSE provider=%s text=%.500s",
                     llm_result.provider, llm_result.text)

        try:
            parsed = json.loads(llm_result.text)
        except json.JSONDecodeError as exc:
            # Gemini occasionally wraps JSON in markdown fences.
            cleaned = re.sub(r"^```(?:json)?\s*", "", llm_result.text.strip())
            cleaned = re.sub(r"\s*```$", "", cleaned)
            try:
                parsed = json.loads(cleaned)
            except json.JSONDecodeError:
                raise ValueError(
                    f"LLM returned non-JSON: {llm_result.text[:200]}"
                ) from exc

        if not isinstance(parsed, dict):
            raise ValueError(f"LLM returned non-object JSON: {type(parsed)}")

        # Stamp provider so normalize() can log it.
        parsed["_provider"] = llm_result.provider
        logger.info("INTENT PARSED provider=%s keys=%s", llm_result.provider, list(parsed.keys()))
        return parsed

    def _build_prompt(self, text: str, is_query: bool = False) -> str:
        return f"""You classify personal knowledge notes by intent.

Current date: {date.today().isoformat()}
Input type: {"query" if is_query else "note"}

Return STRICT JSON with exactly these keys and NO other text:

  intent_type   — one of: communication, todo, study, reminder, idea,
                  reference, question, event, general
  action        — verb describing the action, or null
  actor         — person or organisation involved, or null
  topic         — the main subject/domain (e.g. "PostgreSQL", "Docker",
                  "AI", "Finance"), or null if none
  subtopic      — a narrower aspect within the topic (e.g. "Indexing",
                  "Containers"), or null if not applicable
  object        — what the action is applied to, or null
  temporal_text — time reference string (e.g. "tomorrow", "next week"), or null
  urgency       — one of: low, medium, high
  confidence    — float in [0.0, 1.0]

Rules:
- intent_type must be exactly one of the listed values.
- actor is a real person or org name, NOT a generic word like "team" or "project".
- topic should be a SHORT noun (1-3 words max), reusable across notes.
  BAD: "PostgreSQL Query Optimization and Indexing"
  GOOD: "PostgreSQL"
- subtopic is optional detail within the topic.
  BAD: "Query Optimization" if it duplicates the topic
  GOOD: "Indexing", "Transactions", "Replication"
- urgency must be exactly low / medium / high.
- confidence must be a decimal number between 0 and 1.
- Return JSON only. No markdown. No explanation.

Examples:
  "Tell Sid about the internship"
  → {{"intent_type":"communication","action":"tell","actor":"Sid","topic":null,"subtopic":null,"object":"internship","temporal_text":null,"urgency":"medium","confidence":0.95}}

  "Study PostgreSQL indexing strategies"
  → {{"intent_type":"study","action":"study","actor":null,"topic":"PostgreSQL","subtopic":"Indexing","object":"indexing strategies","temporal_text":null,"urgency":"medium","confidence":0.92}}

  "Buy groceries tomorrow"
  → {{"intent_type":"todo","action":"buy","actor":null,"topic":"Shopping","subtopic":null,"object":"groceries","temporal_text":"tomorrow","urgency":"high","confidence":0.97}}

  "Docker container networking"
  → {{"intent_type":"reference","action":null,"actor":null,"topic":"Docker","subtopic":"Networking","object":"container networking","temporal_text":null,"urgency":"low","confidence":0.88}}

  "Idea for a startup around AI resume review"
  → {{"intent_type":"idea","action":null,"actor":null,"topic":"AI","subtopic":"Resume","object":"startup idea","temporal_text":null,"urgency":"low","confidence":0.85}}

Input:
{text}
"""

    # ------------------------------------------------------------------
    # Validation + normalization
    # ------------------------------------------------------------------

    def _normalize(self, data: dict, text: str) -> dict:
        """
        Validate and sanitise every field from an LLM response.

        All fixes are logged at WARNING level so issues are traceable.
        No malformed value should propagate past this method.
        """
        repairs: list[str] = []

        intent_type = self._validate_intent_type(
            data.get("intent_type"), repairs
        )
        action = self._clean_token(data.get("action"), _LEN_ACTION, "action", repairs)
        actor = self._clean_actor(data.get("actor"), repairs)
        topic = self._clean_short_text(data.get("topic"), _LEN_TOPIC, "topic", repairs)
        subtopic = self._clean_short_text(data.get("subtopic"), _LEN_SUBTOPIC, "subtopic", repairs)
        obj = self._clean_short_text(data.get("object"), _LEN_OBJECT, "object", repairs)
        temporal = self._clean_short_text(
            data.get("temporal_text"), _LEN_TEMPORAL, "temporal_text", repairs
        )
        urgency = self._validate_urgency(data.get("urgency"), repairs)
        confidence = self._validate_confidence(data.get("confidence"), repairs)
        due_date = self._parse_due_date(data.get("due_date"))

        # Weak-object guard: if the LLM returned a useless object, infer one.
        if self._is_weak_object(obj, intent_type):
            inferred = self._clean_short_text(
                self._infer_object(text, action, actor),
                _LEN_OBJECT, "object(inferred)", repairs
            )
            if not self._is_weak_object(inferred, intent_type):
                obj = inferred

        if repairs:
            logger.warning(
                "INTENT VALIDATION REPAIRS note_preview=%.60s repairs=%s",
                text,
                repairs,
            )

        return {
            "intent_type": intent_type,
            "action": action,
            "actor": actor,
            "topic": topic,
            "subtopic": subtopic,
            "object": obj,
            "due_date": due_date,
            "temporal_text": temporal,
            "urgency": urgency,
            "category_hint": None,
            "confidence": confidence,
            "reasoning_summary": self._clean_short_text(
                data.get("reasoning_summary"), 500, "reasoning_summary", repairs
            ),
            "raw_llm_json": {
                k: v for k, v in data.items() if k != "_provider"
            },
            "model_name": data.get("_provider", "unknown"),
            "prompt_version": self.PROMPT_VERSION,
            "source_text": text,
        }

    # --- Validators ----------------------------------------------------

    def _validate_intent_type(
        self, value: object, repairs: list[str]
    ) -> str:
        raw = self._strip_safe(value)
        if raw is None:
            repairs.append("intent_type=None → general")
            return "general"
        lowered = raw.lower()
        if lowered in VALID_INTENT_TYPES:
            return lowered
        # Try synonym map.
        mapped = INTENT_TYPE_SYNONYMS.get(lowered)
        if mapped:
            repairs.append(f"intent_type={raw!r} → {mapped} (synonym)")
            return mapped
        repairs.append(f"intent_type={raw!r} → general (unknown)")
        return "general"

    def _validate_urgency(self, value: object, repairs: list[str]) -> str:
        raw = self._strip_safe(value)
        if raw is None:
            repairs.append("urgency=None → medium")
            return "medium"
        lowered = raw.lower()[:_LEN_URGENCY]
        if lowered in VALID_URGENCY:
            return lowered
        # Fuzzy repair: contains the valid word anywhere.
        for v in ("high", "low", "medium"):
            if v in lowered:
                repairs.append(f"urgency={raw!r} → {v} (fuzzy)")
                return v
        repairs.append(f"urgency={raw!r} → medium (unknown)")
        return "medium"

    def _validate_confidence(self, value: object, repairs: list[str]) -> float:
        try:
            f = float(value)  # type: ignore[arg-type]
        except (TypeError, ValueError):
            repairs.append(f"confidence={value!r} → 0.5 (unparseable)")
            return 0.5
        clamped = max(0.0, min(1.0, f))
        if clamped != f:
            repairs.append(f"confidence={f} → {clamped} (clamped)")
        return round(clamped, 4)

    def _clean_actor(self, value: object, repairs: list[str]) -> str | None:
        text = self._strip_safe(value)
        if text is None:
            return None
        if text.lower() in {"self", "me", "myself", "none", "null", "n/a", "user"}:
            repairs.append(f"actor={text!r} → None (self-reference)")
            return None
        if "/" in text or "," in text:
            repairs.append(f"actor={text!r} → None (composite)")
            return None
        if len(text) > _LEN_ACTOR:
            repairs.append(f"actor truncated {len(text)} → {_LEN_ACTOR}")
            text = text[:_LEN_ACTOR]
        return text.title()

    def _clean_token(
        self, value: object, max_len: int, field: str, repairs: list[str]
    ) -> str | None:
        text = self._strip_safe(value)
        if text is None:
            return None
        lowered = text.lower()
        if len(lowered) > max_len:
            repairs.append(f"{field} truncated {len(lowered)} → {max_len}")
            lowered = lowered[:max_len]
        return lowered or None

    def _clean_short_text(
        self, value: object, max_len: int, field: str, repairs: list[str]
    ) -> str | None:
        text = self._strip_safe(value)
        if text is None:
            return None
        if len(text) > max_len:
            repairs.append(f"{field} truncated {len(text)} → {max_len}")
            text = text[:max_len]
        return text or None

    @staticmethod
    def _strip_safe(value: object) -> str | None:
        """
        Convert to clean string or return None.

        Rejects:
        - dict/list (LLM returned structured value instead of string)
        - empty/whitespace-only strings
        - null synonyms
        - strings containing only invisible Unicode (zero-width spaces etc.)
        """
        if value is None:
            return None
        if isinstance(value, (dict, list)):
            return None
        text = str(value).strip()
        if not text or text.lower() in {"null", "none", "n/a", ""}:
            return None
        # Remove invisible Unicode control characters and zero-width spaces.
        text = "".join(
            ch for ch in text
            if unicodedata.category(ch) not in ("Cf", "Cc")
        ).strip()
        return text or None

    # --- Object inference ----------------------------------------------

    def _infer_object(
        self, text: str, action: str | None, actor: str | None
    ) -> str | None:
        cleaned = text
        if action:
            cleaned = re.sub(
                rf"^\s*{re.escape(action)}\b", "", cleaned, flags=re.IGNORECASE
            ).strip()
        if actor:
            cleaned = re.sub(
                rf"\b(?:to|with|for)\s+{re.escape(actor)}\b",
                "", cleaned, flags=re.IGNORECASE,
            ).strip()
            cleaned = re.sub(
                rf"^\s*{re.escape(actor)}\b", "", cleaned, flags=re.IGNORECASE
            ).strip()
        cleaned = re.sub(r"\s+", " ", cleaned)
        cleaned = re.sub(
            r"^(about|regarding|for)\s+", "", cleaned, flags=re.IGNORECASE
        )
        return cleaned[:_LEN_OBJECT] or None

    def _is_weak_object(self, value: str | None, intent_type: str | None) -> bool:
        if not value:
            return True
        lowered = value.strip().lower()
        if lowered in self.GENERIC_OBJECT_WORDS:
            return True
        if intent_type and lowered == intent_type:
            return True
        return len(lowered) < 3

    # --- Date parsing --------------------------------------------------

    def _parse_due_date(self, value: object) -> date | None:
        if not value:
            return None
        if isinstance(value, date):
            return value
        try:
            return datetime.strptime(str(value), "%Y-%m-%d").date()
        except (ValueError, TypeError):
            return None

    # ------------------------------------------------------------------
    # Rule-based fallback classifier
    # ------------------------------------------------------------------

    def _extract_with_rules(self, text: str) -> dict:
        logger.warning("RULE-BASED EXTRACTION ACTIVATED text=%.80s", text)

        lowered = text.lower()
        words = re.findall(r"\b[a-zA-Z0-9']+\b", lowered)
        word_set = set(words)

        intent_type = "general"
        confidence = 0.55

        reminder_kws = {"remind", "reminder", "reminders", "remember"}
        event_kws = {"event", "events", "meeting", "meetings", "scheduled", "schedule"}
        question_kws = {"what", "how", "why", "when", "where", "who", "which", "is", "are", "does", "do"}

        comm = self._find_communication_request(text)
        actor = None
        if comm:
            action, actor = comm
            intent_type = "communication"
            confidence = 0.70 if actor else 0.62
        elif any(w in self.COMMUNICATION_ACTIONS for w in words):
            intent_type = "communication"
            actor = (
                self._find_actor_after_preposition(text)
                or self._find_title_name(text)
            )
            confidence = 0.72 if actor else 0.62
        elif any(w in {"study", "learn", "practice", "revise", "learning"} for w in words):
            intent_type = "study"
            confidence = 0.65
        elif word_set & reminder_kws:
            intent_type = "reminder"
            confidence = 0.65
        elif word_set & event_kws:
            intent_type = "event"
            confidence = 0.65
        elif any(w in self.TODO_ACTIONS for w in words) or self._has_time_marker(lowered) or any(phrase in lowered for phrase in ["need to", "have to", "should", "must", "todo", "to-do", "task", "tasks"]):
            intent_type = "todo"
            confidence = 0.65
        elif any(w in {"idea", "ideas", "startup", "concept", "concepts", "brainstorm"} for w in words):
            intent_type = "idea"
            confidence = 0.60
        elif any(w in {"reference", "references", "docs", "documentation"} for w in words):
            intent_type = "reference"
            confidence = 0.60
        elif word_set & question_kws:
            intent_type = "question"
            confidence = 0.60

        first_word = words[0] if words else ""
        action = first_word if first_word in (self.COMMUNICATION_ACTIONS | self.TODO_ACTIONS) else None

        if not actor:
            inferred_actor = self._find_actor_after_preposition(text) or self._find_title_name(text)
            if inferred_actor and inferred_actor.lower() not in self._ACTOR_GENERIC_WORDS:
                actor = inferred_actor

        actor = self._clean_actor(actor, [])

        topic = None
        for word in words:
            if word in self.TECH_MAP:
                topic = self.TECH_MAP[word]
                break

        if not topic:
            caps = re.findall(r"\b[A-Z][a-zA-Z]+\b", text)
            first_raw = text.split()[0] if text.split() else ""
            if caps and caps[0] == first_raw:
                caps = caps[1:]
            for cap in caps:
                if cap.lower() not in self._ACTOR_GENERIC_WORDS and (not actor or cap.lower() != actor.lower()):
                    topic = cap
                    break

        due_date, temporal_text = self._infer_due_date(lowered)

        result = {
            "intent_type": intent_type,
            "action": action,
            "actor": actor,
            "topic": topic,
            "subtopic": None,
            "object": self._infer_object(text, action, actor),
            "due_date": due_date,
            "temporal_text": temporal_text,
            "urgency": "high" if due_date else "medium",
            "category_hint": None,
            "confidence": confidence,
            "reasoning_summary": "Heuristic fallback classification.",
            "raw_llm_json": None,
            "model_name": "heuristic",
            "prompt_version": self.PROMPT_VERSION,
            "source_text": text,
        }

        logger.info(
            "RULE RESULT intent=%s action=%s actor=%s topic=%s confidence=%.2f",
            intent_type,
            action,
            actor,
            topic,
            confidence,
        )
        return result

    # --- Rule helpers --------------------------------------------------

    def _find_actor_after_preposition(self, text: str) -> str | None:
        match = re.search(
            r"\b(?:to|about|with|for)\s+([A-Z][a-zA-Z]+)\b", text
        )
        return match.group(1) if match else None

    def _find_communication_request(
        self, text: str
    ) -> tuple[str, str | None] | None:
        action_pattern = "|".join(self.COMMUNICATION_ACTIONS)
        match = re.search(rf"\b({action_pattern})\s+([A-Z][a-zA-Z]+)\b", text)
        if match:
            return match.group(1).lower(), match.group(2)
        match = re.search(
            rf"\b({action_pattern})\b.*\b(?:to|with|for)\s+([A-Z][a-zA-Z]+)\b",
            text,
        )
        if match:
            return match.group(1).lower(), match.group(2)
        return None

    def _find_title_name(self, text: str) -> str | None:
        matches = re.findall(r"\b[A-Z][a-zA-Z]+\b", text)
        return matches[1] if len(matches) >= 2 else None

    def _has_time_marker(self, lowered: str) -> bool:
        return any(
            marker in lowered
            for marker in ["today", "tomorrow", "by ", "before ", "next "]
        )

    def _infer_due_date(
        self, lowered: str
    ) -> tuple[date | None, str | None]:
        today = date.today()

        if "tomorrow" in lowered:
            return today + timedelta(days=1), "tomorrow"

        month_match = re.search(
            r"\b(?:by|on|before)?\s*"
            r"(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)"
            r"[a-z]*\s+(\d{1,2})\b",
            lowered,
        )
        if month_match:
            month_idx = [
                "jan", "feb", "mar", "apr", "may", "jun",
                "jul", "aug", "sep", "oct", "nov", "dec",
            ].index(month_match.group(1)) + 1
            day = int(month_match.group(2))
            year = today.year
            try:
                parsed = date(year, month_idx, day)
            except ValueError:
                return None, month_match.group(0).strip()
            if parsed < today:
                parsed = date(year + 1, month_idx, day)
            return parsed, month_match.group(0).strip()

        return None, None

    # ------------------------------------------------------------------
    # Fast classifier helpers
    # ------------------------------------------------------------------

    def _extract_pseudo_topic(
        self,
        words: list[str],
        intent_type: str,
        actor: str | None,
    ) -> str | None:
        """
        Extract meaningful content tokens for use as a pseudo-topic in
        query signatures.  The same 4-word cap as the old _extract_pseudo_object.
        """
        exclude = self.QUERY_STOPWORDS | {intent_type}
        if actor:
            exclude = exclude | {actor.lower()}

        content_words = [
            w for w in words
            if w not in exclude and len(w) > 1
        ]
        return " ".join(content_words[:4]) or None

    def _find_query_actor(self, words: list[str]) -> str | None:
        """
        Three-pass actor extraction for communication queries (no LLM).

        Pass 1 — token immediately after a communication keyword.
        Pass 2 — token after to/with/for when a comm keyword precedes it.

        Returning None is always safer than returning a wrong actor.
        """
        comm_kw = self.QUERY_COMMUNICATION_KEYWORDS
        # Pass 1: post-verb position.
        for i, word in enumerate(words):
            if word in comm_kw and i + 1 < len(words):
                candidate = words[i + 1]
                if (
                    candidate not in self.QUERY_STOPWORDS
                    and candidate not in self._ACTOR_GENERIC_WORDS
                    and len(candidate) > 1
                ):
                    logger.debug("Actor pass-1 (post-verb): %s", candidate)
                    return self._clean_actor(candidate, [])

        # Pass 2: post-preposition when a comm keyword exists in query.
        if any(w in comm_kw for w in words):
            for i, word in enumerate(words):
                if word in {"to", "with", "for"} and i + 1 < len(words):
                    candidate = words[i + 1]
                    if (
                        candidate not in self.QUERY_STOPWORDS
                        and candidate not in self._ACTOR_GENERIC_WORDS
                        and len(candidate) > 1
                    ):
                        logger.debug("Actor pass-2 (post-prep): %s", candidate)
                        return self._clean_actor(candidate, [])

        logger.debug("Actor extraction: no plausible actor found")
        return None
