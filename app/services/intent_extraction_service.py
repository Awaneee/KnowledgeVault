import json
import logging
import re
from datetime import date
from datetime import datetime
from datetime import timedelta

from app.services.llm_service import LLMService


logger = logging.getLogger(__name__)


class IntentExtractionService:
    PROMPT_VERSION = "intent-v1"
    MODEL_NAME = LLMService.INTENT_MODEL

    INTENT_TYPES = {
        "communication",
        "todo",
        "study",
        "reminder",
        "idea",
        "reference",
        "question",
        "event",
        "general"
    }

    COMMUNICATION_ACTIONS = {
        "tell",
        "inform",
        "discuss",
        "ask",
        "message",
        "call",
        "email",
        "share",
        "meet"
    }

    TODO_ACTIONS = {
        "do",
        "finish",
        "prepare",
        "submit",
        "buy",
        "eat",
        "take",
        "revise",
        "complete",
        "practice",
        "study"
    }

    # --- Query-time fast classifier (no LLM) ---------------------------
    # Used only by extract_query_intent_fast(). Keyword-anchored rather
    # than capitalization-anchored, since chat queries are typically
    # lowercase ("things to tell sid", "what should i tell sid").

    QUERY_COMMUNICATION_KEYWORDS = {
        "tell",
        "inform",
        "discuss",
        "ask",
        "message",
        "call",
        "email",
        "share",
        "meet",
        "talk"
    }

    QUERY_TODO_KEYWORDS = {
        "todo",
        "to-do",
        "task",
        "tasks",
        "pending",
        "finish",
        "complete",
        "submit",
        "buy",
        "pay"
    }

    QUERY_STUDY_KEYWORDS = {
        "study",
        "studies",
        "learn",
        "learning",
        "revise",
        "revision",
        "practice"
    }

    QUERY_IDEA_KEYWORDS = {
        "idea",
        "ideas",
        "startup",
        "concept",
        "concepts",
        "brainstorm"
    }

    QUERY_REFERENCE_KEYWORDS = {
        "reference",
        "references",
        "docs",
        "documentation",
        "notes"
    }

    QUERY_EVENT_KEYWORDS = {
        "event",
        "events",
        "meeting",
        "meetings",
        "scheduled",
        "schedule"
    }

    QUERY_REMINDER_KEYWORDS = {
        "remind",
        "reminder",
        "reminders",
        "appointment",
        "appointments"
    }

    QUERY_QUESTION_KEYWORDS = {
        "what",
        "how",
        "why",
        "when",
        "where",
        "who",
        "which"
    }

    # Checked in priority order: first matching group wins. Communication
    # is checked first since "tell sid" style phrasing is the most
    # actor-specific and most common Ask query in practice.
    QUERY_INTENT_KEYWORD_GROUPS = (
        ("communication", QUERY_COMMUNICATION_KEYWORDS),
        ("reminder", QUERY_REMINDER_KEYWORDS),
        ("study", QUERY_STUDY_KEYWORDS),
        ("idea", QUERY_IDEA_KEYWORDS),
        ("reference", QUERY_REFERENCE_KEYWORDS),
        ("event", QUERY_EVENT_KEYWORDS),
        ("todo", QUERY_TODO_KEYWORDS)
    )

    # Words stripped out before scanning for a leftover actor name in a
    # query like "things to tell sid about the internship".
    QUERY_STOPWORDS = {
        "i", "me", "my", "what", "should", "do", "need", "to", "the",
        "a", "an", "about", "for", "with", "on", "is", "are", "of",
        "things", "thing", "tell", "inform", "discuss", "ask", "message",
        "call", "email", "share", "meet", "talk", "todo", "to-do", "task",
        "tasks", "pending", "finish", "complete", "submit", "buy", "pay",
        "study", "studies", "learn", "learning", "revise", "revision",
        "practice", "idea", "ideas", "startup", "concept", "concepts",
        "brainstorm", "reference", "references", "docs", "documentation",
        "notes", "note", "event", "events", "meeting", "meetings",
        "scheduled", "schedule", "remind", "reminder", "reminders",
        "appointment", "appointments"
    }

    def extract(
        self,
        title: str,
        content: str | None
    ) -> dict:
        text = self._build_text(title, content)

        logger.info(
            "\n%s\nINTENT EXTRACTION INPUT\n%s\n%s",
            "=" * 80,
            "=" * 80,
            text
        )

        try:
            llm_result = self._extract_with_llm(text)
            return self._normalize(llm_result, text)
        except Exception as exc:
            logger.exception(
                "INTENT EXTRACTION FAILED\nERROR: %s\n\nFALLING BACK TO RULES",
                exc
            )
            return self._extract_with_rules(text)

    def extract_query_intent(
        self,
        query: str
    ) -> dict:
        try:
            llm_result = self._extract_with_llm(query, is_query=True)
            return self._normalize(llm_result, query)
        except Exception:
            return self._extract_with_rules(query)

    def extract_query_intent_fast(
        self,
        query: str
    ) -> dict:
        """
        Lightweight, keyword-based intent classifier for Ask-time queries.

        No LLM call — pure regex/keyword matching, runs in microseconds.
        Used by IntentCategoryService.find_categories_for_query() so that
        Ask retrieval never has to wait on Phi3. Accuracy is intentionally
        looser than the LLM path (extract_query_intent); this only needs
        to be good enough to route to the right category, and falls back
        to a vector search anyway if it can't find an exact rule match.
        """
        logger.info("FAST QUERY CLASSIFIER ACTIVATED (no LLM)")

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

        actor = None
        if intent_type == "communication":
            actor = self._find_query_actor(words)
            if actor:
                confidence = 0.72

        result = {
            "intent_type": intent_type,
            "action": next(iter(word_set & self.QUERY_COMMUNICATION_KEYWORDS), None)
            if intent_type == "communication" else None,
            "actor": actor,
            "object": None,
            "due_date": None,
            "temporal_text": None,
            "urgency": "medium",
            "category_hint": None,
            "confidence": confidence,
            "reasoning_summary": "Fast keyword-based query classification.",
            "raw_llm_json": None,
            "model_name": "heuristic-fast",
            "prompt_version": self.PROMPT_VERSION,
            "source_text": query
        }

        logger.info(
            "FAST QUERY RESULT: intent_type=%s actor=%s confidence=%s",
            intent_type,
            actor,
            confidence
        )

        return result

    def _find_query_actor(
        self,
        words: list[str]
    ) -> str | None:
        """
        Picks the most likely actor name out of a lowercase query's
        remaining words after stripping known stopwords/keywords.
        Takes the last leftover word, since actor names in these query
        patterns ("things to tell sid", "what should i tell sid about
        the internship") tend to appear right after the action keyword
        and before any trailing "about X" object.
        """
        leftover = [w for w in words if w not in self.QUERY_STOPWORDS]

        if not leftover:
            return None

        return leftover[0]

    def _build_text(
        self,
        title: str,
        content: str | None
    ) -> str:
        if content:
            return f"{title}\n{content}"
        return title

    def _extract_with_llm(
        self,
        text: str,
        is_query: bool = False
    ) -> dict:
        prompt = f"""
You classify personal knowledge notes by intent.

Current date: {date.today().isoformat()}
Input type: {"query" if is_query else "note"}

Return STRICT JSON with exactly these keys:
intent_type
action
actor
object
due_date
temporal_text
urgency
category_hint
confidence
reasoning_summary

Allowed intent types:
communication
todo
study
reminder
idea
reference
question
event
general

IMPORTANT:
Classify based on WHY the note exists,
not simply what topic it mentions.

Examples:

Communication:
Tell Sid about internship
→ communication
Inform Sid about capstone
→ communication
Discuss project with Sid
→ communication
Email Google support
→ communication
Call professor tomorrow
→ communication

Todo:
Pay rent
→ todo
Buy groceries
→ todo
Eat medicine tomorrow
→ todo
Prepare for test by July 16
→ todo
Complete assignment
→ todo
Revise OOP
→ todo

Study:
Learn graph algorithms
→ study
Practice dynamic programming
→ study
Study operating systems
→ study

Reference:
Docker Containers
→ reference
Redis Caching
→ reference
Machine Learning Embeddings
→ reference
Repository Pattern
→ reference
Transformer Attention Mechanism
→ reference
PostgreSQL Indexing
→ reference

Idea:
Idea for interview preparation app
→ idea
Build AI resume reviewer
→ idea
Startup idea around MCP servers
→ idea
Design a new dress collection
→ idea
Painting concept for portfolio
→ idea

Question:
How does Kafka work?
→ question
What is JWT?
→ question

Event:
Team agreed to use PostgreSQL
→ event
Meeting with professor on Monday
→ event
Capstone review scheduled for July 10
→ event

Reminder:
Call mom tomorrow
→ reminder
Renew driving license next week
→ reminder
Doctor appointment tomorrow
→ reminder

Rules:
- due_date must be ISO YYYY-MM-DD or null.
- actor is the person or organization involved if any.
- confidence must be between 0 and 1.
- category_hint should be short and human friendly.
- Return JSON only.
- Do not invent information.
- No markdown.
- No explanation outside JSON.

Input:
{text}
"""

        response = LLMService.generate(
            prompt=prompt,
            response_format="json",
            model=LLMService.INTENT_MODEL
            
            
        )

        logger.info("OLLAMA RAW RESPONSE:\n%s", response)

        parsed = json.loads(response)
        logger.info("PARSED INTENT JSON:\n%s", parsed)

        return parsed

    def _normalize(
        self,
        data: dict,
        text: str
    ) -> dict:
        intent_type = self._clean_token(
            data.get("intent_type")
        )

        if intent_type not in self.INTENT_TYPES:
            intent_type = "general"

        action = self._clean_token(
            data.get("action")
        )

        actor = self._clean_actor(
            data.get("actor")
        )

        due_date = self._parse_due_date(
            data.get("due_date")
        )

        confidence = self._parse_confidence(
            data.get("confidence")
        )

        return {
            "intent_type": intent_type,
            "action": action,
            "actor": actor,
            "object": self._clean_text(data.get("object")),
            "due_date": due_date,
            "temporal_text": self._clean_text(data.get("temporal_text")),
            "urgency": self._clean_token(data.get("urgency")) or "medium",
            "category_hint": self._clean_text(data.get("category_hint")),
            "confidence": confidence,
            "reasoning_summary": self._clean_text(
                data.get("reasoning_summary")
            ),
            "raw_llm_json": data,
            "model_name": self.MODEL_NAME,
            "prompt_version": self.PROMPT_VERSION,
            "source_text": text
        }

    def _extract_with_rules(
        self,
        text: str
    ) -> dict:
        logger.warning("RULE-BASED EXTRACTION ACTIVATED")

        lowered = text.lower()
        words = re.findall(r"\b[a-zA-Z]+\b", text)
        first_word = words[0].lower() if words else ""

        intent_type = "general"
        action = first_word or None
        actor = None
        confidence = 0.55

        query_communication = self._find_communication_request(text)

        if query_communication:
            action, actor = query_communication
            intent_type = "communication"
            confidence = 0.7 if actor else 0.62
        elif first_word in self.COMMUNICATION_ACTIONS:
            intent_type = "communication"
            actor = self._find_actor_after_preposition(text) or self._find_title_name(text)
            confidence = 0.72 if actor else 0.62
        elif first_word in self.TODO_ACTIONS or self._has_time_marker(lowered):
            intent_type = "todo"
            confidence = 0.65

            if first_word in {"study", "practice"}:
                intent_type = "study"

        if "to do" in lowered or "need to do" in lowered:
            intent_type = "todo"
            action = "do"
            confidence = max(confidence, 0.66)

        due_date, temporal_text = self._infer_due_date(lowered)

        result = {
            "intent_type": intent_type,
            "action": action,
            "actor": actor,
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
            "source_text": text
        }

        logger.info(
            "Detected intent_type: %s\n"
            "Detected action: %s\n"
            "Detected actor: %s\n"
            "Confidence: %s",
            intent_type,
            action,
            actor,
            confidence
        )
        logger.info(
            "RULE RESULT:\n%s",
            json.dumps(
                {
                    "intent_type": intent_type,
                    "action": action,
                    "actor": actor,
                    "confidence": confidence
                },
                indent=4
            )
        )

        return result

    def _find_actor_after_preposition(
        self,
        text: str
    ) -> str | None:
        match = re.search(
            r"\b(?:to|about|with|for)\s+([A-Z][a-zA-Z]+)\b",
            text
        )

        if match:
            return match.group(1)

        return None

    def _find_communication_request(
        self,
        text: str
    ) -> tuple[str, str | None] | None:
        action_pattern = "|".join(self.COMMUNICATION_ACTIONS)
        match = re.search(
            rf"\b({action_pattern})\s+([A-Z][a-zA-Z]+)\b",
            text
        )

        if match:
            return match.group(1).lower(), match.group(2)

        match = re.search(
            rf"\b({action_pattern})\b.*\b(?:to|with|for)\s+([A-Z][a-zA-Z]+)\b",
            text
        )

        if match:
            return match.group(1).lower(), match.group(2)

        return None

    def _find_title_name(
        self,
        text: str
    ) -> str | None:
        matches = re.findall(r"\b[A-Z][a-zA-Z]+\b", text)
        if len(matches) >= 2:
            return matches[1]
        return None

    def _infer_object(
        self,
        text: str,
        action: str | None,
        actor: str | None
    ) -> str | None:
        cleaned = text

        if action:
            cleaned = re.sub(
                rf"^\s*{re.escape(action)}\b",
                "",
                cleaned,
                flags=re.IGNORECASE
            ).strip()

        if actor:
            cleaned = re.sub(
                rf"\b(?:to|with|for)\s+{re.escape(actor)}\b",
                "",
                cleaned,
                flags=re.IGNORECASE
            ).strip()
            cleaned = re.sub(
                rf"^\s*{re.escape(actor)}\b",
                "",
                cleaned,
                flags=re.IGNORECASE
            ).strip()

        cleaned = re.sub(r"\s+", " ", cleaned)
        cleaned = re.sub(
            r"^(about|regarding|for)\s+",
            "",
            cleaned,
            flags=re.IGNORECASE
        )
        return cleaned[:255] or None

    def _infer_due_date(
        self,
        lowered: str
    ) -> tuple[date | None, str | None]:
        today = date.today()

        if "tomorrow" in lowered:
            return today + timedelta(days=1), "tomorrow"

        month_match = re.search(
            r"\b(?:by|on|before)?\s*"
            r"(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)"
            r"[a-z]*\s+(\d{1,2})\b",
            lowered
        )

        if month_match:
            month = [
                "jan",
                "feb",
                "mar",
                "apr",
                "may",
                "jun",
                "jul",
                "aug",
                "sep",
                "oct",
                "nov",
                "dec"
            ].index(month_match.group(1)) + 1
            day = int(month_match.group(2))
            year = today.year

            try:
                parsed = date(year, month, day)
            except ValueError:
                return None, month_match.group(0).strip()

            if parsed < today:
                parsed = date(year + 1, month, day)

            return parsed, month_match.group(0).strip()

        return None, None

    def _has_time_marker(
        self,
        lowered: str
    ) -> bool:
        return any(
            marker in lowered
            for marker in ["today", "tomorrow", "by ", "before ", "next "]
        )

    def _parse_due_date(
        self,
        value
    ) -> date | None:
        if not value:
            return None

        if isinstance(value, date):
            return value

        try:
            return datetime.strptime(str(value), "%Y-%m-%d").date()
        except ValueError:
            return None

    def _parse_confidence(
        self,
        value
    ) -> float:
        try:
            confidence = float(value)
        except (TypeError, ValueError):
            return 0.5

        return min(max(confidence, 0.0), 1.0)

    def _clean_token(
        self,
        value
    ) -> str | None:
        if not value:
            return None

        cleaned = str(value).strip().lower().replace(" ", "_")
        return cleaned[:80] or None

    def _clean_actor(
        self,
        value
    ) -> str | None:
        cleaned = self._clean_text(value)

        if not cleaned or cleaned.lower() in {"self", "me", "myself", "none"}:
            return None

        return cleaned[:120]

    def _clean_text(
        self,
        value
    ) -> str | None:
        if value is None:
            return None

        cleaned = str(value).strip()

        if not cleaned or cleaned.lower() in {"null", "none", "n/a"}:
            return None

        return cleaned