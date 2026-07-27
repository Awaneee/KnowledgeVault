import re

from app.services.llm_service import AllProvidersExhausted
from app.services.llm_service import LLMService


class TitleGenerationService:
    MAX_TITLE_LENGTH = 80

    def generate(
        self,
        content: str
    ) -> tuple[str, str]:
        try:
            title = self._generate_with_llm(content)
            if title:
                return title, "llm"
        except Exception:
            pass

        return self._generate_with_rules(content), "heuristic"

    def _generate_with_llm(
        self,
        content: str
    ) -> str | None:
        prompt = f"""
Generate a concise title for this personal note.

Rules:
- Use title case.
- Maximum 8 words.
- Do not add quotes.
- Return only the title.

Note:
{content}
"""

        response = LLMService.generate(prompt=prompt)
        return self._clean_title(response)

    def _generate_with_rules(
        self,
        content: str
    ) -> str:
        words = re.findall(r"\b[\w'-]+\b", content.strip())
        title_words = words[:8]

        if not title_words:
            return "Untitled Note"

        title = " ".join(title_words).title()
        return self._clean_title(title) or "Untitled Note"

    def _clean_title(
        self,
        value: str | None
    ) -> str | None:
        if not value:
            return None

        cleaned = value.strip().strip("\"'")
        cleaned = re.sub(r"\s+", " ", cleaned)

        if not cleaned:
            return None

        return cleaned[:self.MAX_TITLE_LENGTH]
