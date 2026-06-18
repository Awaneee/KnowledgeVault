import json
import re
from datetime import date
from datetime import datetime
from datetime import timedelta

from app.services.llm_service import LLMService


class IntentExtractionService:
    PROMPT_VERSION = "intent-v1"
    MODEL_NAME = LLMService.MODEL

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

    def extract(
        self,
        title: str,
        content: str | None
    ) -> dict:
        text = self._build_text(title, content)

        try:
            llm_result = self._extract_with_llm(text)
            return self._normalize(llm_result, text)
        except Exception:
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

Return strict JSON with exactly these keys:
intent_type, action, actor, object, due_date, temporal_text, urgency,
category_hint, confidence, reasoning_summary.

Rules:
- intent_type must be one of: communication, todo, study, reminder, idea,
  reference, question, event, general.
- due_date must be ISO YYYY-MM-DD or null.
- actor is the person or group involved, or null.
- confidence is a number from 0 to 1.
- category_hint should be a short human category name.
- Use todo for practical tasks such as "Revise OOP", "Eat medicine tomorrow",
  and "Prepare for test by July 16".
- Use communication when the user needs to tell, inform, discuss, ask, message,
  call, email, or share something with a person.
- Return JSON only.

Input:
{text}
"""

        response = LLMService.generate(
            prompt=prompt,
            response_format="json"
        )

        return json.loads(response)

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

        return {
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
