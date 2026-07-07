import re
from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.core.embedding_model import embedding_model
from app.models.intent_category import IntentCategory
from app.models.note_intent import NoteIntent
from app.models.notes import Note
from app.repositories.intent_category_repository import IntentCategoryRepository
from app.repositories.intent_repository import IntentRepository
from app.services.intent_extraction_service import IntentExtractionService


@dataclass(frozen=True)
class CategoryMatch:
    category: IntentCategory
    score: float
    method: str
    distance: float | None = None


class IntentCategoryService:
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"

    # ---------------------------------------------------------------------------
    # Similarity threshold
    # ---------------------------------------------------------------------------
    # Cosine distance cutoff for category vector search.  Categories further
    # away than this value are excluded from results.
    #
    # Cosine distance for all-MiniLM-L6-v2 on English text (approximate):
    #   < 0.20  — near-paraphrase ("what should I buy" vs "things to buy")
    #   0.20–0.40 — same topic, different phrasing
    #   0.40–0.60 — related domain, loose semantic overlap
    #   0.60–0.80 — different topics with some shared vocabulary
    #   > 0.80  — essentially unrelated
    #
    # 0.55 is a provisional starting value. Richer query signatures place
    # correct matches at ~0.20–0.40 and wrong
    # matches at 0.60+.  0.55 sits between these populations.
    #
    # TO CALIBRATE: inspect category distances during retrieval and set this
    # near the upper bound for correct matches. If recall drops because valid
    # categories are excluded, raise the threshold. If wrong categories keep
    # winning, lower it.
    CATEGORY_SIMILARITY_THRESHOLD: float = 0.55

    # ---------------------------------------------------------------------------
    # Candidate limits
    # ---------------------------------------------------------------------------
    # VECTOR_CANDIDATE_LIMIT controls how many categories the embedding search
    # fetches before merging with the exact rule match.  It is intentionally
    # larger than the public `limit` parameter of find_categories_for_query()
    # (default 3) so that the merge step has enough candidates to work with
    # when the exact rule match is not in the top-N by cosine distance.
    #
    # Tradeoff: a higher value gives the merge step more choices but causes
    # Postgres to score more rows.  5 is appropriate because:
    # - typical users have fewer than 10 active categories
    # - threshold filtering further reduces the effective set
    # - the public API still returns at most `limit` (default 3) categories,
    #   so the note-pool size seen by the caller does not grow
    VECTOR_CANDIDATE_LIMIT: int = 5
    BROAD_EXACT_INTENTS = {"todo", "study", "reference", "question", "idea", "event"}

    GENERIC_CATEGORY_WORDS = {
        "general", "misc", "miscellaneous", "note", "notes", "task", "tasks",
        "thing", "things", "item", "items", "stuff", "topic", "topics",
        "work", "personal", "todo", "to-do", "reminder", "reference",
        "question", "idea", "event", "study", "learn", "learning"
    }

    TOPIC_SYNONYMS = {
        "ai": "Artificial Intelligence",
        "artificial intelligence": "Artificial Intelligence",
        "llm": "Artificial Intelligence",
        "llms": "Artificial Intelligence",
        "large language model": "Artificial Intelligence",
        "large language models": "Artificial Intelligence",
        "ml": "Machine Learning",
        "postgres": "PostgreSQL",
        "postgresql": "PostgreSQL",
        "dbms": "Database Systems",
        "database": "Database Systems",
        "databases": "Database Systems",
        "groceries": "Shopping",
        "grocery": "Shopping",
        "shopping": "Shopping",
        "buy milk": "Shopping",
        "electricity bill": "Bills",
        "water bill": "Bills",
        "rent": "Bills",
        "bills": "Bills"
    }

    TODO_LABEL_KEYWORDS = (
        ("Shopping", {"buy", "purchase", "shop", "shopping", "grocery", "groceries", "milk", "bread", "eggs"}),
        ("Bills", {"pay", "bill", "bills", "rent", "electricity", "water", "internet", "recharge", "subscription", "invoice"}),
        ("Appointments", {"appointment", "doctor", "dentist", "meeting", "reservation", "booking", "schedule"}),
        ("Errands", {"pickup", "pick", "drop", "collect", "deliver", "return", "bank", "post", "courier"})
    )

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
        """Return ordered category objects for callers that do not need scores."""
        return [
            match.category
            for match in self.find_category_matches_for_query(
                query=query,
                user_id=user_id,
                limit=limit
            )
        ]

    def find_category_matches_for_query(
        self,
        query: str,
        user_id: int,
        limit: int = 3
    ) -> list[CategoryMatch]:
        """
        Return scored category matches for a query.

        Hybrid retrieval uses these scores to fuse intent and semantic
        evidence. The public find_categories_for_query() method is preserved
        for existing callers that only need ordered category objects.
        """
        intent = self.extractor.extract_query_intent_fast(query)

        exact_match = self.category_repo.find_rule_match(
            user_id=user_id,
            intent_type=intent["intent_type"],
            actor=intent["actor"]
        )

        canonical_match = self.category_repo.find_by_name(
            user_id=user_id,
            name=self._generate_category_name(intent),
            intent_type=intent["intent_type"]
        )

        signature = self._intent_signature(intent, query=query)
        vector = embedding_model.encode(signature).tolist()

        vector_candidates = self.category_repo.search_by_embedding_with_distance(
            user_id=user_id,
            query_vector=vector,
            limit=self.VECTOR_CANDIDATE_LIMIT,
            max_distance=self.CATEGORY_SIMILARITY_THRESHOLD
        )

        return _score_category_matches(
            exact_match=exact_match,
            canonical_match=canonical_match,
            vector_candidates=vector_candidates,
            intent=intent,
            limit=limit
        )

    # ---------------------------------------------------------------------------
    # Private helpers
    # ---------------------------------------------------------------------------

    # Maximum number of intent categories a single user can have.
    # Without a cap, every unique actor/intent combination creates a
    # new category indefinitely. At scale this produces hundreds of
    # near-duplicate categories ("Work Tasks", "Work Items", etc.)
    # that degrade retrieval quality and slow category search queries.
    # When the cap is reached we fall back to the closest vector match
    # regardless of the compatibility check, so notes still get
    # categorized — just into the best existing bucket rather than a
    # new one.
    MAX_CATEGORIES_PER_USER = 50

    def _find_or_create_category(
        self,
        user_id: int,
        intent: dict
    ) -> tuple[IntentCategory, str]:
        intent = self._normalize_intent_fields(intent)

        # Intent types that are expected to produce multiple topic-specific
        # categories (one per subject, not one per intent_type) must NOT
        # short-circuit on an existing coarse rule match.  If they did,
        # every "study" note would land in the first broad study bucket
        # regardless of topic, defeating the per-topic naming in
        # _generate_category_name.
        #
        # Communication categories remain actor-specific and DO use the
        # rule match so that "Things to Tell Sid" is reused correctly.
        #
        # todo/reminder/event only bypass the rule match when the note
        # carries a distinct object — without one they fall into the
        # generic bucket as before.
        TOPIC_INTENT_TYPES = {
            "study",
            "reference",
            "question",
            "idea",
            "todo",
            "reminder",
            "event"
        }

        intent_type = intent["intent_type"]
        name = self._generate_category_name(intent)
        has_topic = self._has_meaningful_topic(intent)
        skip_rule_match = intent_type in TOPIC_INTENT_TYPES and has_topic

        category = self.category_repo.find_by_name(
            user_id=user_id,
            name=name,
            intent_type=intent_type
        )

        if category:
            return category, "canonical_name"

        if not skip_rule_match:
            # Exact rule match on ingestion is correct for communication and
            # generic (actor-less, topic-less) buckets.
            category = self.category_repo.find_rule_match(
                user_id=user_id,
                intent_type=intent_type,
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
                limit=1,
                max_distance=self.CATEGORY_SIMILARITY_THRESHOLD
            )

            if candidates:
                candidate = candidates[0]
                if self._compatible(candidate, intent):
                    return candidate, "vector"

        # Check category count before creating a new one.
        current_count = self.category_repo.count_by_user(user_id)
        if current_count >= self.MAX_CATEGORIES_PER_USER:
            vector = embedding_model.encode(
                self._intent_signature(intent)
            ).tolist()

            # Cap-fallback deliberately does NOT apply the threshold:
            # when the cap is reached we must assign the note somewhere.
            fallback = self.category_repo.search_by_embedding(
                user_id=user_id,
                query_vector=vector,
                limit=1
            )

            if fallback:
                return fallback[0], "cap_fallback"

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
        intent: dict,
        query: str | None = None
    ) -> str:
        normalized_label = self._derive_topic_label(intent)
        parts = [
            intent.get("intent_type"),
            intent.get("action"),
            intent.get("actor"),
            normalized_label,
            intent.get("object"),
            intent.get("temporal_text"),
        ]
        if query:
            parts.append(query)

        return " ".join(part for part in parts if part)

    def _generate_category_name(
        self,
        intent: dict
    ) -> str:
        """
        Generate a stable, human-readable category name from normalized scalar
        fields. Structured values and generic placeholders are filtered before
        they can become category labels.
        """
        return self._normalized_category_name(
            intent_type=str(intent.get("intent_type") or "general"),
            actor=self._normalize_actor(intent.get("actor")),
            action=str(intent.get("action") or ""),
            label=self._derive_topic_label(intent)
        )

    def _normalized_category_name(
        self,
        intent_type: str,
        actor: str | None,
        action: str | None,
        label: str | None
    ) -> str:
        if intent_type == "communication" and actor:
            if action == "ask":
                return f"Questions for {actor}"
            return f"Things to Tell {actor}"

        if (
            intent_type == "reminder"
            and label
            and label.lower() in {"medicine", "medicines", "health"}
        ):
            return "Health Reminders"

        if intent_type == "todo" and label:
            return label[:100]

        base_names = {
            "todo": "Tasks",
            "study": "Study",
            "reminder": "Reminders",
            "question": "Questions",
            "idea": "Ideas",
            "reference": "Reference",
            "event": "Events",
            "general": "Knowledge"
        }
        base = base_names.get(intent_type, "Knowledge")

        if label:
            if label.lower() == base.lower():
                return base
            return f"{base} - {label}"[:100]

        return base or "General"

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

    def _derive_topic_label(self, intent: dict) -> str | None:
        raw = intent.get("object") or intent.get("category_hint")
        if isinstance(raw, (dict, list)):
            raw = None

        label = self._normalize_label(str(raw or ""))

        if not label:
            label = self._normalize_label(
                self._object_from_source_text(
                    source_text=str(intent.get("source_text") or ""),
                    intent_type=str(intent.get("intent_type") or ""),
                    action=str(intent.get("action") or ""),
                    actor=intent.get("actor")
                )
            )

        if intent.get("intent_type") == "todo" and label:
            label = self._todo_label(label, intent.get("action"))

        if label and label.lower() == str(intent.get("intent_type") or "").lower():
            return None

        return label

    def _has_meaningful_topic(self, intent: dict) -> bool:
        label = self._derive_topic_label(intent)
        return bool(label and label.lower() not in self.GENERIC_CATEGORY_WORDS)

    def _normalize_label(self, value: str | None) -> str | None:
        if not value:
            return None

        cleaned = value.strip()
        if not cleaned:
            return None

        cleaned = re.sub(r"[{}\[\]\"']", " ", cleaned)
        cleaned = re.sub(r"\b\w+\s*:", " ", cleaned)
        cleaned = re.sub(
            r"\b(items?|object|category|hint|note|notes)\b",
            " ",
            cleaned,
            flags=re.IGNORECASE
        )
        cleaned = re.sub(r"\s+", " ", cleaned).strip(" -_:;,.")

        if not cleaned:
            return None

        lowered = cleaned.lower()
        lowered = re.sub(
            r"\b(the|a|an|my|our|your|to|about|for|with|on|in|of)\b",
            " ",
            lowered
        )
        lowered = re.sub(r"\s+", " ", lowered).strip()

        if not lowered or lowered in self.GENERIC_CATEGORY_WORDS:
            return None

        if lowered in self.TOPIC_SYNONYMS:
            return self.TOPIC_SYNONYMS[lowered]

        words = [
            word for word in lowered.split()
            if word not in self.GENERIC_CATEGORY_WORDS
        ]

        if not words:
            return None

        compact = " ".join(words[:5])
        if compact in self.TOPIC_SYNONYMS:
            return self.TOPIC_SYNONYMS[compact]

        return self._humanize_label(compact)

    def _todo_label(self, label: str, action: str | None) -> str:
        tokens = set(
            re.findall(
                r"[a-z0-9]+",
                f"{action or ''} {label}".lower()
            )
        )

        for category, keywords in self.TODO_LABEL_KEYWORDS:
            if tokens & keywords:
                return category

        return label

    def _object_from_source_text(
        self,
        source_text: str,
        intent_type: str,
        action: str,
        actor: str | None
    ) -> str | None:
        if not source_text:
            return None

        cleaned = source_text.strip()
        if action:
            cleaned = re.sub(
                rf"^\s*{re.escape(action)}\b",
                "",
                cleaned,
                flags=re.IGNORECASE
            )
        if actor:
            cleaned = re.sub(
                rf"\b{re.escape(actor)}\b",
                "",
                cleaned,
                flags=re.IGNORECASE
            )

        intent_words = {
            "todo": r"\b(to\s*do|task|tasks|need to|must|should)\b",
            "study": r"\b(study|learn|revise|practice)\b",
            "reference": r"\b(reference|docs?|documentation|notes?)\b",
            "question": r"\b(what|how|why|when|where|who|which|is|are|does|do)\b",
            "idea": r"\b(idea|concept|brainstorm|build|create)\b",
            "event": r"\b(event|meeting|scheduled|schedule)\b",
            "reminder": r"\b(remind|reminder|remember)\b"
        }
        pattern = intent_words.get(intent_type)
        if pattern:
            cleaned = re.sub(pattern, " ", cleaned, flags=re.IGNORECASE)

        cleaned = re.sub(r"\s+", " ", cleaned).strip(" -_:;,.")
        return cleaned[:120] or None

    def _humanize_label(self, value: str) -> str:
        acronym_words = {
            "ai", "api", "jwt", "mcp", "dbms", "sql", "nosql", "ui", "ux"
        }
        brand_words = {
            "kafka": "Kafka",
            "docker": "Docker",
            "redis": "Redis",
            "postgresql": "PostgreSQL",
            "postgres": "PostgreSQL",
            "fastapi": "FastAPI",
            "ollama": "Ollama"
        }

        words = []
        for word in value.split():
            lower = word.lower()
            if lower in brand_words:
                words.append(brand_words[lower])
            elif lower in acronym_words:
                words.append(lower.upper())
            else:
                words.append(lower.capitalize())

        return " ".join(words)

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


def _score_category_matches(
    exact_match: IntentCategory | None,
    canonical_match: IntentCategory | None,
    vector_candidates: list[tuple[IntentCategory, float]],
    intent: dict,
    limit: int
) -> list[CategoryMatch]:
    by_id: dict[int, CategoryMatch] = {}

    def upsert(
        category: IntentCategory,
        score: float,
        method: str,
        distance: float | None = None
    ) -> None:
        current = by_id.get(category.id)
        if current is None or score > current.score:
            by_id[category.id] = CategoryMatch(
                category=category,
                score=score,
                method=method,
                distance=distance
            )

    for category, distance in vector_candidates:
        semantic_score = max(0.0, 1.0 - float(distance))
        if category.intent_type == intent["intent_type"]:
            semantic_score += 0.08
        if category.actor and intent.get("actor"):
            if category.actor.lower() == intent["actor"].lower():
                semantic_score += 0.08
        upsert(
            category=category,
            score=min(1.0, semantic_score),
            method="vector",
            distance=float(distance)
        )

    if exact_match is not None:
        exact_score = 0.92
        if (
            exact_match.intent_type in IntentCategoryService.BROAD_EXACT_INTENTS
            and exact_match.actor is None
            and intent.get("object")
        ):
            exact_score = 0.68
        upsert(
            category=exact_match,
            score=exact_score,
            method="exact_rule"
        )

    if canonical_match is not None:
        upsert(
            category=canonical_match,
            score=0.96,
            method="canonical_name"
        )

    return sorted(
        by_id.values(),
        key=lambda match: (
            match.score,
            match.category.note_count or 0,
            -(match.distance or 0.0),
            -match.category.id
        ),
        reverse=True
    )[:limit]
