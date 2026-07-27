"""
Intent category service.

Responsibilities
----------------
- Assign each processed note to an intent category.
- Generate deterministic, concise category names (≤ 4 words) from validated
  intent metadata — the LLM never names categories.
- Maximise category reuse: semantic search before any new category is created.
- Expose query-time category lookup for hybrid retrieval.

Category naming rules
---------------------
  communication + actor   → "Communication - {Actor}"
  communication + no actor → "Communication"
  study + topic            → "Study - {Topic}"
  study + no topic         → "Study"
  reference + topic        → "Reference - {Topic}"
  reference + no topic     → "Reference"
  idea + topic             → "Ideas - {Topic[:2 words]}"
  idea + no topic          → "Ideas"
  todo + mapped bucket     → Shopping | Bills | Appointments | Errands
  todo + no bucket         → "Tasks"
  reminder                 → "Reminders" (or "Appointments" for medical)
  question + topic         → "Questions - {Topic}"
  question + no topic      → "Questions"
  event + actor            → "Meetings - {Actor}"
  event + topic            → "Meetings"
  general + topic          → "{Topic[:3 words]}"
  general + no topic       → "General"

All names are hard-capped to 4 words before storage.
"""

import logging
import re
import time
from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.embedding_model import embedding_model
from app.models.intent_category import IntentCategory
from app.models.note_intent import NoteIntent
from app.models.notes import Note
from app.repositories.intent_category_repository import IntentCategoryRepository
from app.repositories.intent_repository import IntentRepository
from app.services.intent_extraction_service import IntentExtractionService


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class CategoryMatch:
    category: IntentCategory
    score: float
    method: str
    distance: float | None = None


class IntentCategoryService:
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"

    # ------------------------------------------------------------------
    # Thresholds
    # ------------------------------------------------------------------
    # Cosine-distance cutoffs (all-MiniLM-L6-v2, English text):
    #   < 0.20  near-paraphrase
    #   0.20–0.40  same topic, different phrasing
    #   0.40–0.60  related domain, loose overlap
    #   > 0.60  essentially different topics
    #
    # INGEST_REUSE_THRESHOLD — used when deciding whether to reuse an
    # existing category during indexing.  Kept tight (0.40) to prevent
    # accidentally merging truly different topics.
    #
    # QUERY_SIMILARITY_THRESHOLD — used during retrieval where a wider
    # net improves recall.  0.55 sits between correct (~0.20-0.40) and
    # wrong (0.60+) matches for typical retrieval queries.
    INGEST_REUSE_THRESHOLD: float = 0.40
    QUERY_SIMILARITY_THRESHOLD: float = 0.55

    VECTOR_CANDIDATE_LIMIT: int = 5

    # Intent types that should create per-topic categories rather than
    # one broad bucket per intent type.
    TOPIC_INTENT_TYPES = {
        "study", "reference", "question", "idea", "todo", "reminder", "event",
    }

    # Intent types that are so broad (exact rule match is acceptable) they
    # should NOT override the rule match with a vector result.
    BROAD_EXACT_INTENTS = {
        "todo", "study", "reference", "question", "idea", "event",
    }

    MAX_CATEGORIES_PER_USER = 50

    # ---- Todo bucket keywords ----------------------------------------
    TODO_LABEL_KEYWORDS = (
        ("Shopping", {"buy", "purchase", "shop", "shopping", "grocery", "groceries",
                      "milk", "bread", "eggs", "vegetables", "fruits"}),
        ("Bills", {"pay", "bill", "bills", "rent", "electricity", "water", "internet",
                   "recharge", "subscription", "invoice", "fee", "payment"}),
        ("Appointments", {"appointment", "doctor", "dentist", "meeting", "reservation",
                          "booking", "schedule", "clinic", "hospital"}),
        ("Errands", {"pickup", "pick", "drop", "collect", "deliver", "return",
                     "bank", "post", "courier", "errand"}),
        ("Health", {"medicine", "medication", "pill", "vitamin", "exercise", "gym",
                    "workout", "health", "diet", "sleep"}),
        ("Finance", {"invest", "investment", "stock", "stocks", "mutual", "fund",
                     "loan", "emi", "tax", "budget", "finance", "financial"}),
        ("Travel", {"travel", "trip", "flight", "hotel", "visa", "passport",
                    "booking", "pack", "luggage"}),
    )

    # ---- Brand / acronym humanization --------------------------------
    _BRAND_WORDS: dict[str, str] = {
        "kafka": "Kafka",
        "docker": "Docker",
        "redis": "Redis",
        "postgresql": "PostgreSQL",
        "postgres": "PostgreSQL",
        "fastapi": "FastAPI",
        "ollama": "Ollama",
        "mongodb": "MongoDB",
        "sqlite": "SQLite",
        "mysql": "MySQL",
        "nginx": "Nginx",
        "kubernetes": "Kubernetes",
        "terraform": "Terraform",
        "react": "React",
        "nextjs": "Next.js",
        "flutter": "Flutter",
        "django": "Django",
        "flask": "Flask",
        "celery": "Celery",
        "graphql": "GraphQL",
        "pytorch": "PyTorch",
        "tensorflow": "TensorFlow",
        "langchain": "LangChain",
        "github": "GitHub",
        "gitlab": "GitLab",
        "aws": "AWS",
        "gcp": "GCP",
        "azure": "Azure",
    }
    _ACRONYM_WORDS = {
        "ai", "api", "jwt", "mcp", "dbms", "sql", "nosql",
        "ui", "ux", "http", "https", "rest", "rpc", "rag",
        "llm", "llms", "nlp", "ml",
    }

    # ---- Built-ins / keywords that must never become category names -----
    # These appear when the LLM extracts a Python token (reduce, print, id)
    # or a language keyword as the "topic" of a general-intent note.
    # The set covers all Python 3 built-in functions and a selection of
    # built-in types that commonly appear in code-heavy notes.
    _PYTHON_BUILTINS: frozenset[str] = frozenset({
        "abs", "all", "any", "ascii", "bin", "bool", "breakpoint",
        "bytearray", "bytes", "callable", "chr", "classmethod", "compile",
        "complex", "copyright", "credits", "delattr", "dict", "dir",
        "divmod", "enumerate", "eval", "exec", "exit", "filter", "float",
        "format", "frozenset", "getattr", "globals", "hasattr", "hash",
        "help", "hex", "id", "input", "int", "isinstance", "issubclass",
        "iter", "len", "license", "list", "locals", "map", "max",
        "memoryview", "min", "next", "object", "oct", "open", "ord",
        "pow", "print", "property", "quit", "range", "reduce", "repr",
        "reversed", "round", "set", "setattr", "slice", "sorted",
        "staticmethod", "str", "sum", "super", "tuple", "type", "vars",
        "zip",
    })

    # ---- Topic synonyms (normalize before naming) --------------------
    TOPIC_SYNONYMS: dict[str, str] = {
        "ai": "AI",
        "artificial intelligence": "AI",
        "llm": "AI",
        "llms": "AI",
        "large language model": "AI",
        "large language models": "AI",
        "ml": "Machine Learning",
        "machine learning": "Machine Learning",
        "postgres": "PostgreSQL",
        "postgresql": "PostgreSQL",
        "dbms": "Database Systems",
        "database": "Database",
        "databases": "Database",
        "groceries": "Shopping",
        "grocery": "Shopping",
        "shopping": "Shopping",
        "buy milk": "Shopping",
        "electricity bill": "Bills",
        "water bill": "Bills",
        "rent": "Bills",
        "bills": "Bills",
        "os": "Operating Systems",
        "operating system": "Operating Systems",
        "operating systems": "Operating Systems",
        "ds": "Data Structures",
        "data structure": "Data Structures",
        "data structures": "Data Structures",
        "algo": "Algorithms",
        "algorithms": "Algorithms",
        "dsa": "Data Structures",
        "oop": "OOP",
        "object oriented": "OOP",
        "object-oriented": "OOP",
    }

    GENERIC_CATEGORY_WORDS = {
        "general", "misc", "miscellaneous", "note", "notes", "task", "tasks",
        "thing", "things", "item", "items", "stuff", "topic", "topics",
        "work", "personal", "todo", "to-do", "reminder", "reference",
        "question", "idea", "event", "study", "learn", "learning",
    }

    # ------------------------------------------------------------------
    # Constructor
    # ------------------------------------------------------------------

    def __init__(self, db: Session):
        self.db = db
        self.category_repo = IntentCategoryRepository(db)
        self.intent_repo = IntentRepository(db)
        self.extractor = IntentExtractionService()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def process_note(
        self,
        note_id: int,
        user_id: int,
        title: str,
        content: str | None,
    ) -> dict:
        t0 = time.monotonic()

        intent = self.extractor.extract(title=title, content=content)

        stored_intent = self.intent_repo.create_or_update_note_intent(
            note_id=note_id,
            user_id=user_id,
            data=intent,
        )

        category, method, similarity_score = self._find_or_create_category(
            user_id=user_id,
            intent=intent,
        )

        # category is None only when the per-user cap has been reached.
        # The intent is still stored; the note is retrievable via semantic
        # search.  Skip the assignment and embedding steps entirely so no
        # false category membership is recorded.
        if category is None:
            elapsed = time.monotonic() - t0
            logger.warning(
                "CATEGORY SKIPPED method=cap_hit intent=%s topic=%s "
                "note_id=%d elapsed=%.2fs",
                intent["intent_type"],
                intent.get("topic"),
                note_id,
                elapsed,
            )
            return {
                "intent": stored_intent,
                "category": None,
                "assignment": None,
            }

        assignment = self.intent_repo.create_or_update_assignment(
            note_id=note_id,
            user_id=user_id,
            intent_category_id=category.id,
            confidence=intent["confidence"],
            assignment_method=method,
        )

        self.category_repo.touch_after_assignment(category_id=category.id)

        self._refresh_category_embedding(category=category, intent=intent)

        elapsed = time.monotonic() - t0
        action_word = "REUSED" if method != "created" else "CREATED"
        logger.info(
            "CATEGORY %s name=%r method=%s intent=%s actor=%s topic=%s "
            "note_id=%d elapsed=%.2fs",
            action_word,
            category.name,
            method,
            intent["intent_type"],
            intent.get("actor"),
            intent.get("topic"),
            note_id,
            elapsed,
        )
        logger.info(
            "CATEGORY ASSIGNMENT: note_id=%d, matched_category_id=%d, category_name=%r, "
            "assignment_method=%s, semantic_similarity=%.4f, reuse_confidence=%.4f",
            note_id,
            category.id,
            category.name,
            method,
            similarity_score,
            intent["confidence"]
        )

        return {
            "intent": stored_intent,
            "category": category,
            "assignment": assignment,
        }

    def get_categories(self, user_id: int) -> list[IntentCategory]:
        return self.category_repo.get_all(user_id=user_id)

    def get_notes_for_category(
        self, intent_category_id: int, user_id: int
    ) -> list:
        return self.intent_repo.get_notes_for_category(
            intent_category_id=intent_category_id,
            user_id=user_id,
        )

    def backfill_user_notes(self, user_id: int, limit: int = 100) -> dict:
        notes = (
            self.db.query(Note)
            .outerjoin(NoteIntent, NoteIntent.note_id == Note.id)
            .filter(Note.user_id == user_id, NoteIntent.id.is_(None))
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
                    content=note.content,
                )
                processed += 1
            except Exception:
                logger.exception(
                    "BACKFILL FAILED note_id=%d user_id=%d", note.id, user_id
                )
                self.db.rollback()
                failed += 1

        remaining = (
            self.db.query(Note)
            .outerjoin(NoteIntent, NoteIntent.note_id == Note.id)
            .filter(Note.user_id == user_id, NoteIntent.id.is_(None))
            .count()
        )

        return {"processed": processed, "failed": failed, "remaining_hint": remaining}

    def find_categories_for_query(
        self,
        query: str,
        user_id: int,
        limit: int = 3,
    ) -> list[IntentCategory]:
        """Return ordered category objects for callers that don't need scores."""
        return [
            match.category
            for match in self.find_category_matches_for_query(
                query=query,
                user_id=user_id,
                limit=limit,
            )
        ]

    def find_category_matches_for_query(
        self,
        query: str,
        user_id: int,
        limit: int = 3,
    ) -> list[CategoryMatch]:
        """
        Scored category matches for hybrid retrieval.
        Uses the fast classifier (no LLM) so retrieval never blocks.
        """
        intent = self.extractor.extract_query_intent_fast(query)

        exact_match = self.category_repo.find_rule_match(
            user_id=user_id,
            intent_type=intent["intent_type"],
            actor=intent["actor"],
        )

        category_name = self._generate_category_name(intent)
        canonical_match = self.category_repo.find_by_name(
            user_id=user_id,
            name=category_name,
            intent_type=intent["intent_type"] if intent["intent_type"] != "general" else None,
        )

        signature = self._intent_signature(intent, query=query)
        vector = embedding_model.encode(signature).tolist()

        # A category's embedding may share generic words with a query from a
        # different intent family (for example a Redis study category and a
        # Redis question).  Such a category is not compatible evidence.  The
        # intent type and, where present, actor are hard filters; the vector
        # score only ranks within that compatible set.
        vector_candidates = self.category_repo.search_by_embedding_with_distance(
            user_id=user_id,
            query_vector=vector,
            limit=self.VECTOR_CANDIDATE_LIMIT,
            max_distance=settings.CATEGORY_QUERY_THRESHOLD,
            intent_type=intent["intent_type"] if intent["intent_type"] != "general" else None,
            actor=intent["actor"],
        )

        return _score_category_matches(
            exact_match=exact_match,
            canonical_match=canonical_match,
            vector_candidates=vector_candidates,
            intent=intent,
            limit=limit,
        )

    # ------------------------------------------------------------------
    # Category find-or-create  (Phase 2 — ADR-002)
    # ------------------------------------------------------------------

    # Per-intent-type cosine distance thresholds for semantic reuse.
    # Precise intents (study/reference/question): topic specificity matters.
    # At T=0.30, "Kafka" and "Redis" stay separate (~0.55 apart in embedding space).
    # Broad intents: semantic overlap is acceptable.
    _REUSE_THRESHOLDS: dict[str, float] = {
        "study":         0.30,
        "reference":     0.30,
        "question":      0.30,
        "communication": 0.35,
        "general":       0.35,
        "idea":          0.40,
        "reminder":      0.40,
        "event":         0.40,
        "todo":          0.40,
    }

    def _find_or_create_category(
        self, user_id: int, intent: dict
    ) -> tuple[IntentCategory | None, str, float]:
        intent = self._normalize_intent_fields(intent)
        intent_type = intent["intent_type"]
        name = self._generate_category_name(intent)

        # Step 1 — Exact canonical name match (unchanged, fast path).
        # Handles 34% of notes at 1,055-note scale.
        category = self.category_repo.find_by_name(
            user_id=user_id,
            name=name,
            intent_type=intent_type,
        )
        if category:
            return category, "canonical_name", 1.0

        # Step 2 — Fuzzy vector reuse.
        #
        # Rule-match is retired: diagnostic showed 0% hit rate across 1,055 notes
        # because every generic bucket ("Tasks", "General") found by rule-match
        # was already found by canonical name in Step 1.  Removing it eliminates
        # a dead code path without any behavioural change.
        #
        # _compatible() now gates on intent_type + actor only (ADR-002).
        # The old exact topic-string equality check was dead code: it required
        # the same condition as canonical_name (Step 1), so any note satisfying
        # _compatible() would already have been caught above.  The distance
        # threshold T controls topic proximity instead.
        #
        # When CATEGORY_FUZZY_COMPAT_ENABLED=False the strict Phase-1 path runs.
        vector = embedding_model.encode(self._intent_signature(intent)).tolist()

        if settings.CATEGORY_FUZZY_COMPAT_ENABLED:
            threshold = self._reuse_threshold(intent_type)
            candidates = self.category_repo.search_by_embedding_with_distance(
                user_id=user_id,
                query_vector=vector,
                limit=self.VECTOR_CANDIDATE_LIMIT,
                max_distance=threshold,
                intent_type=intent_type,   # hard SQL filter — prevents cross-type merges
                actor=intent.get("actor"), # hard SQL filter for communication categories
            )
            for candidate, distance in candidates:
                if self._compatible(candidate, intent):
                    logger.info(
                        "CATEGORY FUZZY REUSE name=%r distance=%.3f threshold=%.2f",
                        candidate.name, distance, threshold,
                    )
                    return candidate, "vector", 1.0 - float(distance)
        else:
            # Phase 1 fallback: original CATEGORY_INGEST_THRESHOLD, no intent_type filter.
            candidates = self.category_repo.search_by_embedding_with_distance(
                user_id=user_id,
                query_vector=vector,
                limit=3,
                max_distance=settings.CATEGORY_INGEST_THRESHOLD,
            )
            for candidate, distance in candidates:
                if self._compatible_strict(candidate, intent):
                    logger.info(
                        "CATEGORY SEMANTIC REUSE name=%r distance=%.3f",
                        candidate.name, distance,
                    )
                    return candidate, "vector", 1.0 - float(distance)

        # Step 3 — Adaptive cap check.
        # The cap scales with corpus size (NOTES_PER_CAP target, bounded by MIN/MAX).
        # When CATEGORY_ADAPTIVE_CAP_ENABLED=False, falls back to MAX_CATEGORIES_PER_USER=50.
        max_cats = self._adaptive_max_categories(user_id)
        if self.category_repo.count_by_user(user_id) >= max_cats:
            logger.warning(
                "CATEGORY CAP REACHED user_id=%d cap=%d intent=%s topic=%s — "
                "note will be uncategorized rather than force-assigned",
                user_id, max_cats, intent_type, self._resolve_topic_label(intent),
            )
            return None, "cap_hit", 0.0

        # Step 4 — Create category.
        # For general-intent notes with the conservative guard enabled, validate
        # the topic before creating a dedicated category.  LLM-extracted topics
        # for general notes are frequently verbs ("Added"), question fragments
        # ("Does Redis Eviction"), or 2-char tokens.  Those notes are directed to
        # a shared "General" catchall instead of creating a singleton category.
        if intent_type == "general" and settings.CATEGORY_CONSERVATIVE_GENERAL_ENABLED:
            if not self._should_create_general_category(intent):
                catchall = self._get_or_create_general_catchall(user_id)
                logger.info(
                    "GENERAL CATCHALL topic=%r category=%r",
                    self._resolve_topic_label(intent),
                    catchall.name if catchall else None,
                )
                return catchall, "general_catchall", 0.5

        category = self.category_repo.create(
            user_id=user_id,
            name=name,
            intent_type=intent_type,
            actor=intent["actor"],
            action=intent["action"],
            time_scope=self._time_scope(intent),
            description=self._generate_description(intent),
            confidence=intent["confidence"],
        )
        return category, "created", 1.0

    # ------------------------------------------------------------------
    # Adaptive cap and per-intent thresholds
    # ------------------------------------------------------------------

    def _reuse_threshold(self, intent_type: str) -> float:
        """
        Per-intent cosine distance threshold for semantic reuse.

        Configured via CATEGORY_REUSE_THRESHOLD_PRECISE and _BROAD, but
        _REUSE_THRESHOLDS provides per-intent granularity.
        """
        base = self._REUSE_THRESHOLDS.get(intent_type)
        if base is not None:
            return base
        # For study/reference/question use the precise threshold from config
        # (allows runtime tuning without code changes).
        if intent_type in {"study", "reference", "question"}:
            return settings.CATEGORY_REUSE_THRESHOLD_PRECISE
        return settings.CATEGORY_REUSE_THRESHOLD_BROAD

    def _adaptive_max_categories(self, user_id: int) -> int:
        """
        Compute the per-user category cap.

        When CATEGORY_ADAPTIVE_CAP_ENABLED=False: returns MAX_CATEGORIES_PER_USER.

        When enabled: max(MIN, min(MAX, note_count // NOTES_PER_CAP)).
        At 1,055 notes with NOTES_PER_CAP=10: cap = 105.
        At 3,000 notes: cap = 300.
        At 100,000 notes: capped at MAX=2,000.
        """
        if not settings.CATEGORY_ADAPTIVE_CAP_ENABLED:
            return self.MAX_CATEGORIES_PER_USER

        from sqlalchemy import func as sqla_func
        note_count = (
            self.db.query(sqla_func.count(Note.id))
            .filter(Note.user_id == user_id)
            .scalar()
        ) or 0

        cap = note_count // settings.CATEGORY_NOTES_PER_CAP
        return max(
            settings.CATEGORY_ADAPTIVE_CAP_MIN,
            min(settings.CATEGORY_ADAPTIVE_CAP_MAX, cap),
        )

    # ------------------------------------------------------------------
    # General-intent conservation helpers
    # ------------------------------------------------------------------

    def _should_create_general_category(self, intent: dict) -> bool:
        """
        For general-intent notes: is the LLM-extracted topic substantive
        enough to justify a dedicated category?

        Returns True for known brand/tech names and meaningful noun phrases.
        Returns False for single verbs, question fragments, 2-char tokens,
        and other low-quality topic extractions that produce singleton
        categories with no future reuse value.
        """
        import keyword as _kw

        topic = self._resolve_topic_label(intent)
        if not topic:
            return False

        words = topic.lower().split()

        if len(words) == 1:
            w = words[0]
            # Always allow known good single-word terms
            if w in self._BRAND_WORDS or w in self._ACRONYM_WORDS:
                return True
            # Reject Python keywords/built-ins and generic words
            if (_kw.iskeyword(w) or w in self._PYTHON_BUILTINS
                    or w in self.GENERIC_CATEGORY_WORDS):
                return False
            # Reject very short tokens that slipped past _sanitize_category_name
            if len(w) < 4:
                return False
            # Reject common action verbs and auxiliaries that appear as topics
            # when the LLM can't identify the subject of a general note
            _WEAK_WORDS = {
                "added", "changed", "create", "update", "fixed", "removed",
                "deleted", "modified", "refactored", "improved", "does",
                "make", "build", "find", "show", "gets", "sets",
            }
            if w in _WEAK_WORDS:
                return False
            return True

        # Multi-word: reject if it starts with a question word (fragment topics)
        _QUESTION_STARTS = {"does", "are", "what", "why", "how", "when", "is", "can"}
        if words[0] in _QUESTION_STARTS:
            return False

        return True

    def _get_or_create_general_catchall(self, user_id: int) -> IntentCategory | None:
        """
        Return or create a shared 'General' bucket for general-intent notes
        whose topic is not substantive enough to merit a dedicated category.

        Returns None (→ cap_hit behaviour) if the adaptive cap has been reached.
        """
        catchall = self.category_repo.find_by_name(
            user_id=user_id, name="General", intent_type="general",
        )
        if catchall:
            return catchall

        max_cats = self._adaptive_max_categories(user_id)
        if self.category_repo.count_by_user(user_id) >= max_cats:
            return None

        return self.category_repo.create(
            user_id=user_id,
            name="General",
            intent_type="general",
            actor=None,
            action=None,
            time_scope=None,
            description="General notes without a specific identifiable topic.",
            confidence=0.5,
        )

    # ------------------------------------------------------------------
    # Deterministic category naming (Python-only, no LLM)
    # ------------------------------------------------------------------

    def _generate_category_name(self, intent: dict) -> str:
        """
        Generate a stable, human-readable category name ≤ 4 words.
        The LLM extracts topic/actor/intent_type; this method turns those
        into the final name without any LLM involvement.
        """
        intent_type = str(intent.get("intent_type") or "general")
        actor = self._normalize_actor(intent.get("actor"))
        action = str(intent.get("action") or "")

        # Use LLM-extracted topic/subtopic; fall back to object if absent.
        topic = self._resolve_topic_label(intent)

        name = self._build_name(intent_type, actor, action, topic)
        # Hard cap: maximum 4 words regardless of input.
        name = self._cap_words(name, 4)
        # Guard: strip trailing punctuation and reject programming tokens,
        # Python built-ins, and other pathological single-token names.
        return self._sanitize_category_name(name)

    def _build_name(
        self,
        intent_type: str,
        actor: str | None,
        action: str,
        topic: str | None,
    ) -> str:
        """
        Central dispatch table for category names.
        Every branch produces a name ≤ 4 words.  The _cap_words() call in
        _generate_category_name() is a safety net for edge cases.
        """
        t = intent_type

        # Communication ---------------------------------------------------
        if t == "communication":
            if actor:
                return f"Communication - {actor}"
            if topic:
                return f"Communication - {self._cap_words(topic, 2)}"
            return "Communication"

        # Study -----------------------------------------------------------
        if t == "study":
            if topic:
                return f"Study - {self._cap_words(topic, 3)}"
            return "Study"

        # Reference -------------------------------------------------------
        if t == "reference":
            if topic:
                return f"Reference - {self._cap_words(topic, 3)}"
            return "Reference"

        # Idea ------------------------------------------------------------
        if t == "idea":
            if topic:
                return f"Ideas - {self._cap_words(topic, 2)}"
            return "Ideas"

        # Todo ------------------------------------------------------------
        if t == "todo":
            if topic:
                bucket = self._todo_bucket(topic, action)
                if bucket:
                    return bucket
            return "Tasks"

        # Reminder --------------------------------------------------------
        if t == "reminder":
            if topic:
                lowered = topic.lower()
                if any(w in lowered for w in
                       ("medicine", "medication", "doctor", "health", "pill")):
                    return "Appointments"
            return "Reminders"

        # Question --------------------------------------------------------
        if t == "question":
            if topic:
                return f"Questions - {self._cap_words(topic, 2)}"
            return "Questions"

        # Event -----------------------------------------------------------
        if t == "event":
            if actor:
                return f"Meetings - {actor}"
            return "Meetings"

        # General ---------------------------------------------------------
        if topic:
            return self._cap_words(topic, 3)
        return "General"

    def _resolve_topic_label(self, intent: dict) -> str | None:
        """
        Pick the best available topic label from the intent fields,
        normalize it, and return a clean short string or None.

        Priority: topic → subtopic → object → source_text fallback.
        """
        # Prefer explicit topic field (new schema).
        raw = intent.get("topic") or intent.get("subtopic")

        # Fall back to object if topic is absent or generic.
        if not raw or self._is_generic_word(raw):
            raw = intent.get("object") or intent.get("category_hint")

        if not raw or self._is_generic_word(str(raw)):
            raw = self._object_from_source_text(
                source_text=str(intent.get("source_text") or ""),
                intent_type=str(intent.get("intent_type") or ""),
                action=str(intent.get("action") or ""),
                actor=intent.get("actor"),
            )

        return self._normalize_topic(raw)

    def _normalize_topic(self, value: object) -> str | None:
        if value is None or isinstance(value, (dict, list)):
            return None
        cleaned = str(value).strip()
        if not cleaned:
            return None
        lowered = cleaned.lower()
        aliases = {
            "postgres": "PostgreSQL",
            "postgresql": "PostgreSQL",
            "postgres database": "PostgreSQL",
            "postgresql database": "PostgreSQL",
            "postgresql indexing": "PostgreSQL",
            "redis cache": "Redis",
            "redis": "Redis",
            "redis database": "Redis",
            "docker compose": "Docker Compose",
            "compose": "Docker Compose",
            "docker-compose": "Docker Compose",
            "jwt auth": "JWT Authentication",
            "jwt authentication": "JWT Authentication",
            "artificial intelligence": "AI",
            "ai": "AI",
            "large language model": "AI",
            "large language models": "AI",
            "llm": "AI",
            "llms": "AI",
        }
        if lowered in aliases:
            return aliases[lowered]
        return self._normalize_label(value)

    def _normalize_label(self, value: object) -> str | None:
        """
        Clean and normalise a raw topic/object string into a short label.
        """
        if value is None or isinstance(value, (dict, list)):
            return None

        cleaned = str(value).strip()
        if not cleaned:
            return None

        # Strip structural artefacts from LLM responses.
        cleaned = re.sub(r"[{}\[\]\"']", " ", cleaned)
        cleaned = re.sub(r"\b\w+\s*:", " ", cleaned)  # "key: value" → " value"
        cleaned = re.sub(r"\s+", " ", cleaned).strip(" -_:;,.")

        if not cleaned:
            return None

        lowered = cleaned.lower()

        # Check synonym map before any word trimming.
        if lowered in self.TOPIC_SYNONYMS:
            return self.TOPIC_SYNONYMS[lowered]

        # Strip articles/prepositions.
        lowered = re.sub(
            r"\b(the|a|an|my|our|your|to|about|for|with|on|in|of)\b",
            " ",
            lowered,
        )
        lowered = re.sub(r"\s+", " ", lowered).strip()

        if not lowered or lowered in self.GENERIC_CATEGORY_WORDS:
            return None

        # Re-check synonym after article stripping.
        if lowered in self.TOPIC_SYNONYMS:
            return self.TOPIC_SYNONYMS[lowered]

        # Remove generic words.
        words = [w for w in lowered.split() if w not in self.GENERIC_CATEGORY_WORDS]
        if not words:
            return None

        compact = " ".join(words[:4])
        if compact in self.TOPIC_SYNONYMS:
            return self.TOPIC_SYNONYMS[compact]

        return self._humanize_label(compact)

    def _humanize_label(self, value: str) -> str:
        """Apply brand/acronym capitalisation to a space-separated label."""
        result = []
        for word in value.split():
            lower = word.lower()
            if lower in self._BRAND_WORDS:
                result.append(self._BRAND_WORDS[lower])
            elif lower in self._ACRONYM_WORDS:
                result.append(lower.upper())
            else:
                result.append(lower.capitalize())
        return " ".join(result)

    @staticmethod
    def _cap_words(text: str, n: int) -> str:
        """Return the first n words of text, joined by spaces."""
        return " ".join(text.split()[:n])

    def _sanitize_category_name(self, name: str) -> str:
        """
        Strip trailing punctuation and reject pathological single-token names.

        Returns the cleaned name, or "General" when the name is invalid.

        Rejected patterns (all single-token):
        - Python built-ins: "print", "reduce", "id", "map", …
        - Python keywords: "for", "if", "class", "return", …
        - Tokens ≤ 2 characters that are not a known acronym (e.g. "Rs", "Id")
        - Tokens with no alphabetic characters at all

        Multi-token names ("Study - PostgreSQL", "Communication - Sid") are
        never rejected here; their components were already validated upstream
        by _normalize_label and _normalize_actor.
        """
        import keyword

        # Strip trailing sentence-ending punctuation that the LLM occasionally
        # appends (e.g. "Flutter Application Performance.").
        cleaned = name.strip().rstrip(".,;:!?\"'")
        if not cleaned:
            return "General"

        # Single-token guard only — multi-word names are safe.
        if " " not in cleaned and " - " not in cleaned:
            lower = cleaned.lower()
            if keyword.iskeyword(lower):
                logger.warning(
                    "CATEGORY NAME SANITIZED reason=python_keyword name=%r → General",
                    name,
                )
                return "General"
            if lower in self._PYTHON_BUILTINS:
                logger.warning(
                    "CATEGORY NAME SANITIZED reason=python_builtin name=%r → General",
                    name,
                )
                return "General"
            # Very short tokens that are not known good acronyms (e.g. "Rs", "Id").
            if len(cleaned) <= 2 and lower not in self._ACRONYM_WORDS:
                logger.warning(
                    "CATEGORY NAME SANITIZED reason=too_short name=%r → General",
                    name,
                )
                return "General"
            # Tokens with no alphabetic characters (e.g. "42", "---").
            if not any(c.isalpha() for c in cleaned):
                logger.warning(
                    "CATEGORY NAME SANITIZED reason=no_alpha name=%r → General",
                    name,
                )
                return "General"

        return cleaned

    def _todo_bucket(self, topic: str, action: str) -> str | None:
        """Map a todo's topic/action to a reusable bucket label."""
        tokens = set(
            re.findall(r"[a-z0-9]+", f"{action} {topic}".lower())
        )
        for label, keywords in self.TODO_LABEL_KEYWORDS:
            if tokens & keywords:
                return label
        return None

    def _is_generic_word(self, value: str) -> bool:
        return (value or "").strip().lower() in self.GENERIC_CATEGORY_WORDS

    # ------------------------------------------------------------------
    # Intent compatibility + normalization helpers
    # ------------------------------------------------------------------

    def _get_topic_from_category_name(self, name: str, intent_type: str) -> str | None:
        if not name:
            return None
        name_str = str(name)
        if " - " in name_str:
            parts = name_str.split(" - ", 1)
            prefix = parts[0].strip().lower()
            if prefix in {"communication", "meetings"}:
                return None
            return parts[1].strip()
        else:
            lowered = name_str.strip().lower()
            generic_buckets = {
                "study", "reference", "ideas", "tasks", "reminders", 
                "questions", "meetings", "general", "communication",
                "shopping", "bills", "appointments", "errands", "health", "finance", "travel"
            }
            if lowered in generic_buckets:
                return None
            return name_str.strip()

    def _compatible(self, category: IntentCategory, intent: dict) -> bool:
        """
        Phase 2 compatibility check (ADR-002): intent_type + actor gates only.

        The exact topic-string equality check from Phase 1 has been removed.
        It was structurally dead code: it required the same condition as
        canonical_name matching (Step 1 of _find_or_create_category), so any
        note satisfying _compatible() would already have been caught by
        canonical_name.

        Topic proximity is now controlled by the per-intent cosine distance
        threshold in _reuse_threshold().  At T=0.30, "Kafka" and "Redis" study
        notes remain in separate categories (~0.55 apart); near-miss LLM variants
        like "k8s" vs "Kubernetes" correctly reuse (<0.20 apart).

        Investigation evidence:
        - Cross-intent merges at T=0.40 (without intent_type gate): 5% same-type purity
        - Keeping intent_type as a hard gate prevents those 95% wrong-type merges
        - The SQL query in _find_or_create_category already pre-filters by intent_type
          and actor; _compatible() is a Python-level guard after the DB result arrives
        """
        # Hard gate 1: intent type must match.
        if category.intent_type != intent["intent_type"]:
            return False
        # Hard gate 2: actor must match for communication categories.
        # "Communication - Sid" must not absorb messages intended for "Siddhant"
        # even when their embedding signatures are close (shared vocabulary).
        if category.actor and intent.get("actor"):
            if category.actor.lower() != intent["actor"].lower():
                return False
        elif bool(category.actor) != bool(intent.get("actor")):
            return False
        return True

    def _compatible_strict(self, category: IntentCategory, intent: dict) -> bool:
        """
        Phase 1 fallback: adds exact topic-string equality on top of _compatible().
        Used when CATEGORY_FUZZY_COMPAT_ENABLED=False for full backwards compatibility.
        This check is structurally dead code for topic-bearing intents (see ADR-002)
        but preserves the exact Phase 1 behaviour when the flag is off.
        """
        if not self._compatible(category, intent):
            return False
        intent_topic = self._normalize_topic(self._resolve_topic_label(intent))
        category_topic = self._normalize_topic(
            self._get_topic_from_category_name(category.name, category.intent_type)
        )
        return (intent_topic or "").lower().strip() == (category_topic or "").lower().strip()

    def _normalize_intent_fields(self, intent: dict) -> dict:
        normalized = dict(intent)
        normalized["actor"] = self._normalize_actor(intent.get("actor"))
        return normalized

    def _normalize_actor(self, value: object) -> str | None:
        if value is None or isinstance(value, (dict, list)):
            return None
        cleaned = re.sub(r"\s+", " ", str(value)).strip()
        if not cleaned or cleaned.lower() in {"self", "me", "myself", "none"}:
            return None
        if "/" in cleaned or "," in cleaned:
            return None
        return cleaned.title()[:120]

    def _has_meaningful_topic(self, intent: dict) -> bool:
        label = self._resolve_topic_label(intent)
        return bool(label and label.lower() not in self.GENERIC_CATEGORY_WORDS)

    def _intent_signature(self, intent: dict, query: str | None = None) -> str:
        """
        Build a text string that captures the semantic identity of an intent.
        This is what gets embedded to find/compare categories.
        """
        topic_label = self._resolve_topic_label(intent)
        parts = [
            intent.get("intent_type"),
            intent.get("action"),
            intent.get("actor"),
            topic_label,
            intent.get("object"),
            intent.get("temporal_text"),
        ]
        if query:
            parts.append(query)
        return " ".join(p for p in parts if p)

    def _refresh_category_embedding(
        self, category: IntentCategory, intent: dict
    ) -> None:
        # Embed the incoming note's semantic signature, not category metadata.
        # Category metadata is static and would produce the same vector on every
        # call, making the embedding useless for distinguishing categories.
        # The intent signature captures what this specific note is about, so
        # folding many of them into a running mean gives a centroid that reflects
        # the full distribution of notes in the category.
        new_vector = embedding_model.encode(
            self._intent_signature(intent)
        ).tolist()

        existing = self.category_repo.get_embedding(category.id)

        if existing is None or existing.centroid_note_count == 0:
            # First note — the embedding IS the centroid; count = 1.
            self.category_repo.upsert_embedding(
                intent_category_id=category.id,
                embedding_model=self.EMBEDDING_MODEL,
                embedding_vector=new_vector,
                centroid_note_count=1,
            )
        else:
            # Incremental mean: c_new = (c_old * N + v_new) / (N + 1)
            # This is O(dim) and adds no extra DB reads beyond the get above.
            n = existing.centroid_note_count
            old_vector = existing.embedding_vector
            centroid = [
                (old * n + new) / (n + 1)
                for old, new in zip(old_vector, new_vector)
            ]
            self.category_repo.upsert_embedding(
                intent_category_id=category.id,
                embedding_model=self.EMBEDDING_MODEL,
                embedding_vector=centroid,
                centroid_note_count=n + 1,
            )

    def _generate_description(self, intent: dict) -> str:
        topic = self._resolve_topic_label(intent)
        if intent.get("actor"):
            return (
                f"Notes with {intent['intent_type']} intent "
                f"involving {intent['actor']}."
            )
        if topic:
            return f"Notes about {topic} ({intent['intent_type']})."
        return f"Notes with {intent['intent_type']} intent."

    def _time_scope(self, intent: dict) -> str | None:
        if intent.get("due_date"):
            return "dated"
        temporal = intent.get("temporal_text")
        if temporal:
            return temporal.lower().replace(" ", "_")[:50]
        return None

    def _object_from_source_text(
        self,
        source_text: str,
        intent_type: str,
        action: str,
        actor: str | None,
    ) -> str | None:
        if not source_text:
            return None
        cleaned = source_text.strip()
        if action:
            cleaned = re.sub(
                rf"^\s*{re.escape(action)}\b", "", cleaned, flags=re.IGNORECASE
            )
        if actor:
            cleaned = re.sub(
                rf"\b{re.escape(actor)}\b", "", cleaned, flags=re.IGNORECASE
            )
        intent_patterns = {
            "todo": r"\b(to\s*do|task|tasks|need to|must|should)\b",
            "study": r"\b(study|learn|revise|practice)\b",
            "reference": r"\b(reference|docs?|documentation|notes?)\b",
            "question": r"\b(what|how|why|when|where|who|which|is|are|does|do)\b",
            "idea": r"\b(idea|concept|brainstorm|build|create)\b",
            "event": r"\b(event|meeting|scheduled|schedule)\b",
            "reminder": r"\b(remind|reminder|remember)\b",
        }
        pattern = intent_patterns.get(intent_type)
        if pattern:
            cleaned = re.sub(pattern, " ", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s+", " ", cleaned).strip(" -_:;,.")
        return cleaned[:120] or None


# ---------------------------------------------------------------------------
# Query-time scoring (module-level to keep IntentCategoryService focused)
# ---------------------------------------------------------------------------

def _score_category_matches(
    exact_match: IntentCategory | None,
    canonical_match: IntentCategory | None,
    vector_candidates: list[tuple[IntentCategory, float]],
    intent: dict,
    limit: int,
) -> list[CategoryMatch]:
    by_id: dict[int, CategoryMatch] = {}

    def upsert(
        category: IntentCategory,
        score: float,
        method: str,
        distance: float | None = None,
    ) -> None:
        current = by_id.get(category.id)
        if current is None or score > current.score:
            by_id[category.id] = CategoryMatch(
                category=category,
                score=score,
                method=method,
                distance=distance,
            )

    # Vector candidates — base score from cosine similarity.
    for category, distance in vector_candidates:
        semantic_score = max(0.0, 1.0 - float(distance))
        # Boost for matching intent type.
        if category.intent_type == intent["intent_type"]:
            semantic_score = min(1.0, semantic_score + 0.08)
        # Boost for matching actor.
        if category.actor and intent.get("actor"):
            if category.actor.lower() == intent["actor"].lower():
                semantic_score = min(1.0, semantic_score + 0.08)
        upsert(category, score=semantic_score, method="vector", distance=float(distance))

    # Exact rule match — high but slightly lower than canonical.
    if exact_match is not None:
        exact_score = 0.92
        # Reduce weight for broad intent types when there is specific topic
        # evidence — prevents a generic "Study" bucket from winning over
        # "Study - PostgreSQL" when the query is clearly topic-specific.
        if (
            exact_match.intent_type in IntentCategoryService.BROAD_EXACT_INTENTS
            and exact_match.actor is None
            and intent.get("object")
        ):
            exact_score = 0.70
        upsert(exact_match, score=exact_score, method="exact_rule")

    # Canonical name match — highest confidence.
    if canonical_match is not None:
        upsert(canonical_match, score=0.96, method="canonical_name")

    return sorted(
        by_id.values(),
        key=lambda m: (
            m.score,
            m.category.note_count or 0,
            -(m.distance or 0.0),
            -m.category.id,
        ),
        reverse=True,
    )[:limit]
