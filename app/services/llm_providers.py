"""
LLM provider implementations.

Provider hierarchy:
  - GeminiProvider  — primary; used for both intent extraction and answer generation.
  - GroqProvider    — secondary; used for ANSWER GENERATION only.
                      Not used for intent extraction because Groq lacks
                      Gemini's schema-enforced JSON mode.
  - OllamaProvider  — local development only; enabled via OLLAMA_ENABLED=true.

All providers implement LLMProvider and raise LLMProviderError on failure.
"""

import json
import logging
from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass, field

import requests

from app.core.config import settings


logger = logging.getLogger(__name__)


class LLMProviderError(RuntimeError):
    """Raised when an LLM provider call fails for any reason."""


@dataclass(frozen=True)
class LLMResult:
    text: str
    provider: str
    model: str
    fallback_events: tuple[str, ...] = field(default_factory=tuple)


class LLMProvider(ABC):
    name: str

    @abstractmethod
    def extract_intent(self, prompt: str) -> LLMResult:
        raise NotImplementedError

    @abstractmethod
    def generate_answer(self, prompt: str, model: str | None = None) -> LLMResult:
        raise NotImplementedError

    def generate_stream(self, prompt: str, model: str | None = None):
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Gemini
# ---------------------------------------------------------------------------

class GeminiProvider(LLMProvider):
    name = "gemini"

    INTENT_SCHEMA = {
        "type": "OBJECT",
        "properties": {
            "intent_type": {"type": "STRING"},
            "action": {"type": "STRING", "nullable": True},
            "actor": {"type": "STRING", "nullable": True},
            "topic": {"type": "STRING", "nullable": True},
            "subtopic": {"type": "STRING", "nullable": True},
            "object": {"type": "STRING", "nullable": True},
            "temporal_text": {"type": "STRING", "nullable": True},
            "urgency": {"type": "STRING"},
            "confidence": {"type": "NUMBER"},
        },
        "required": [
            "intent_type",
            "action",
            "actor",
            "topic",
            "subtopic",
            "object",
            "temporal_text",
            "urgency",
            "confidence",
        ],
    }

    def __init__(self) -> None:
        if not settings.GEMINI_API_KEY:
            raise LLMProviderError("GEMINI_API_KEY is not configured")

    def extract_intent(self, prompt: str) -> LLMResult:
        return self._generate(
            prompt=prompt,
            model=settings.GEMINI_INTENT_MODEL,
            generation_config={
                "temperature": 0,
                "responseMimeType": "application/json",
                "responseSchema": self.INTENT_SCHEMA,
            },
        )

    def generate_answer(self, prompt: str, model: str | None = None) -> LLMResult:
        return self._generate(
            prompt=prompt,
            model=model or settings.GEMINI_ANSWER_MODEL,
            generation_config={"temperature": 0.2},
        )

    def generate_stream(self, prompt: str, model: str | None = None):
        selected_model = model or settings.GEMINI_ANSWER_MODEL
        url = (
            f"{settings.GEMINI_API_BASE}/models/{selected_model}:streamGenerateContent"
            f"?key={settings.GEMINI_API_KEY}"
        )
        payload = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.2},
        }

        try:
            response = requests.post(
                url,
                json=payload,
                timeout=settings.LLM_TIMEOUT_SECONDS,
                stream=True,
            )
            response.raise_for_status()
        except requests.exceptions.Timeout as exc:
            raise LLMProviderError(
                f"Gemini stream timeout after {settings.LLM_TIMEOUT_SECONDS}s"
            ) from exc
        except requests.RequestException as exc:
            raise LLMProviderError(f"Gemini stream request failed: {exc}") from exc

        buffer = ""
        for chunk in response.iter_content(chunk_size=1024, decode_unicode=True):
            if not chunk:
                continue
            buffer += chunk
            while True:
                buffer = buffer.strip()
                if not buffer:
                    break
                if buffer.startswith("["):
                    buffer = buffer[1:].strip()
                    continue
                if buffer.startswith(","):
                    buffer = buffer[1:].strip()
                    continue
                if buffer.startswith("]"):
                    buffer = buffer[1:].strip()
                    break
                try:
                    obj, index = json.JSONDecoder().raw_decode(buffer)
                    try:
                        token = obj["candidates"][0]["content"]["parts"][0]["text"]
                        if token:
                            yield token
                    except (KeyError, IndexError, TypeError):
                        pass
                    buffer = buffer[index:].strip()
                except json.JSONDecodeError:
                    break

    def _generate(
        self,
        prompt: str,
        model: str,
        generation_config: dict | None = None,
    ) -> LLMResult:
        import time
        url = (
            f"{settings.GEMINI_API_BASE}/models/{model}:generateContent"
            f"?key={settings.GEMINI_API_KEY}"
        )
        payload: dict = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        }
        if generation_config:
            payload["generationConfig"] = generation_config

        max_retries = 5
        backoff = 2.0
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    url,
                    json=payload,
                    timeout=settings.LLM_TIMEOUT_SECONDS,
                )
                if response.status_code == 429:
                    logger.warning(
                        "GeminiProvider returned 429 (Rate Limit). Retrying in %.1fs... (attempt %d/%d)",
                        backoff,
                        attempt + 1,
                        max_retries,
                    )
                    time.sleep(backoff)
                    backoff *= 2.0
                    continue
                response.raise_for_status()
                break
            except requests.exceptions.Timeout as exc:
                raise LLMProviderError(
                    f"Gemini timeout after {settings.LLM_TIMEOUT_SECONDS}s"
                ) from exc
            except requests.RequestException as exc:
                if attempt == max_retries - 1:
                    raise LLMProviderError(f"Gemini request failed after retries: {exc}") from exc
                time.sleep(backoff)
                backoff *= 2.0
        else:
            raise LLMProviderError(
                f"Gemini failed after {max_retries} retries due to rate limiting (429)"
            )

        data = response.json()
        try:
            text = data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError, TypeError) as exc:
            raise LLMProviderError(
                f"Gemini response missing text field; raw={str(data)[:200]}"
            ) from exc

        return LLMResult(text=text.strip(), provider=self.name, model=model)


# ---------------------------------------------------------------------------
# Groq — answer generation only, OpenAI-compatible chat API
# ---------------------------------------------------------------------------

class GroqProvider(LLMProvider):
    """
    Groq Chat Completions provider.

    Used for ANSWER GENERATION only. Groq does not support schema-enforced
    JSON output (Gemini's responseSchema), so intent extraction is handled
    by Gemini with a rule-based fallback — never Groq.
    """

    name = "groq"

    # Groq does not implement extract_intent.
    def extract_intent(self, prompt: str) -> LLMResult:
        raise NotImplementedError(
            "GroqProvider does not support intent extraction. "
            "Use GeminiProvider or the rule-based fallback."
        )

    def __init__(self) -> None:
        if not settings.GROQ_API_KEY:
            raise LLMProviderError("GROQ_API_KEY is not configured")

    def generate_answer(self, prompt: str, model: str | None = None) -> LLMResult:
        selected_model = model or settings.GROQ_MODEL
        url = f"{settings.GROQ_API_BASE}/chat/completions"
        payload = {
            "model": selected_model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
        }

        try:
            response = requests.post(
                url,
                json=payload,
                headers={
                    "Authorization": f"Bearer {settings.GROQ_API_KEY}",
                    "Content-Type": "application/json",
                },
                timeout=settings.LLM_TIMEOUT_SECONDS,
            )
            response.raise_for_status()
        except requests.exceptions.Timeout as exc:
            raise LLMProviderError(
                f"Groq timeout after {settings.LLM_TIMEOUT_SECONDS}s"
            ) from exc
        except requests.RequestException as exc:
            raise LLMProviderError(f"Groq request failed: {exc}") from exc

        try:
            data = response.json()
            text = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
            raise LLMProviderError(
                f"Groq response missing content field; raw={response.text[:200]}"
            ) from exc

        return LLMResult(text=text.strip(), provider=self.name, model=selected_model)

    def generate_stream(self, prompt: str, model: str | None = None):
        selected_model = model or settings.GROQ_MODEL
        url = f"{settings.GROQ_API_BASE}/chat/completions"
        payload = {
            "model": selected_model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
            "stream": True,
        }

        try:
            response = requests.post(
                url,
                json=payload,
                headers={
                    "Authorization": f"Bearer {settings.GROQ_API_KEY}",
                    "Content-Type": "application/json",
                },
                timeout=settings.LLM_TIMEOUT_SECONDS,
                stream=True,
            )
            response.raise_for_status()
        except requests.exceptions.Timeout as exc:
            raise LLMProviderError(
                f"Groq stream timeout after {settings.LLM_TIMEOUT_SECONDS}s"
            ) from exc
        except requests.RequestException as exc:
            raise LLMProviderError(f"Groq stream request failed: {exc}") from exc

        for line in response.iter_lines():
            if not line:
                continue
            decoded = line.decode("utf-8") if isinstance(line, bytes) else line
            if decoded.startswith("data: "):
                decoded = decoded[6:]
            if decoded.strip() == "[DONE]":
                break
            try:
                obj = json.loads(decoded)
                token = obj["choices"][0]["delta"].get("content", "")
                if token:
                    yield token
            except (json.JSONDecodeError, KeyError, IndexError, TypeError):
                continue


# ---------------------------------------------------------------------------
# OpenRouter — OpenAI-compatible gateway (answer generation only)
# ---------------------------------------------------------------------------

class OpenRouterProvider(LLMProvider):
    """
    OpenRouter Chat Completions provider.

    Wraps https://openrouter.ai/api/v1/chat/completions — OpenAI-compatible.
    Supports 100+ models including free-tier options (model id ends in :free).
    Used for ANSWER GENERATION only (no schema-enforced JSON for intent).
    """

    name = "openrouter"

    def extract_intent(self, prompt: str) -> LLMResult:
        raise NotImplementedError(
            "OpenRouterProvider does not support intent extraction. "
            "Use GeminiProvider or the rule-based fallback."
        )

    def __init__(self) -> None:
        if not settings.OPENROUTER_API_KEY:
            raise LLMProviderError("OPENROUTER_API_KEY is not configured")

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "X-Title": settings.OPENROUTER_APP_NAME,
        }

    def generate_answer(self, prompt: str, model: str | None = None) -> LLMResult:
        selected_model = model or settings.OPENROUTER_MODEL
        url = f"{settings.OPENROUTER_API_BASE}/chat/completions"
        payload = {
            "model": selected_model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
        }

        try:
            response = requests.post(
                url,
                json=payload,
                headers=self._headers(),
                timeout=settings.LLM_TIMEOUT_SECONDS,
            )
            response.raise_for_status()
        except requests.exceptions.Timeout as exc:
            raise LLMProviderError(
                f"OpenRouter timeout after {settings.LLM_TIMEOUT_SECONDS}s"
            ) from exc
        except requests.RequestException as exc:
            raise LLMProviderError(f"OpenRouter request failed: {exc}") from exc

        try:
            text = response.json()["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
            raise LLMProviderError(
                f"OpenRouter response missing content; raw={response.text[:200]}"
            ) from exc

        return LLMResult(text=text.strip(), provider=self.name, model=selected_model)

    def generate_stream(self, prompt: str, model: str | None = None):
        selected_model = model or settings.OPENROUTER_MODEL
        url = f"{settings.OPENROUTER_API_BASE}/chat/completions"
        payload = {
            "model": selected_model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
            "stream": True,
        }

        try:
            response = requests.post(
                url,
                json=payload,
                headers=self._headers(),
                timeout=settings.LLM_TIMEOUT_SECONDS,
                stream=True,
            )
            response.raise_for_status()
        except requests.exceptions.Timeout as exc:
            raise LLMProviderError(
                f"OpenRouter stream timeout after {settings.LLM_TIMEOUT_SECONDS}s"
            ) from exc
        except requests.RequestException as exc:
            raise LLMProviderError(f"OpenRouter stream request failed: {exc}") from exc

        for line in response.iter_lines():
            if not line:
                continue
            decoded = line.decode("utf-8") if isinstance(line, bytes) else line
            if decoded.startswith("data: "):
                decoded = decoded[6:]
            if decoded.strip() == "[DONE]":
                break
            try:
                obj = json.loads(decoded)
                token = obj["choices"][0]["delta"].get("content", "")
                if token:
                    yield token
            except (json.JSONDecodeError, KeyError, IndexError, TypeError):
                continue


# ---------------------------------------------------------------------------
# Ollama — local development only
# ---------------------------------------------------------------------------

class OllamaProvider(LLMProvider):
    """
    Ollama local inference provider.

    Only included in the provider chain when OLLAMA_ENABLED=true.
    Should never be used in production environments.
    """

    name = "ollama"

    def extract_intent(self, prompt: str) -> LLMResult:
        return self._generate(
            prompt=prompt,
            model=settings.OLLAMA_INTENT_MODEL,
            response_format="json",
        )

    def generate_answer(self, prompt: str, model: str | None = None) -> LLMResult:
        return self._generate(
            prompt=prompt,
            model=model or settings.OLLAMA_ANSWER_MODEL,
        )

    def _generate(
        self,
        prompt: str,
        model: str,
        response_format: str | None = None,
    ) -> LLMResult:
        payload: dict = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0},
        }
        if response_format:
            payload["format"] = response_format

        try:
            response = requests.post(
                settings.OLLAMA_URL,
                json=payload,
                timeout=settings.LLM_TIMEOUT_SECONDS,
            )
            response.raise_for_status()
        except requests.exceptions.Timeout as exc:
            raise LLMProviderError(
                f"Ollama timeout after {settings.LLM_TIMEOUT_SECONDS}s"
            ) from exc
        except requests.RequestException as exc:
            raise LLMProviderError(f"Ollama request failed: {exc}") from exc

        try:
            text = response.json()["response"]
        except (KeyError, TypeError, json.JSONDecodeError) as exc:
            raise LLMProviderError(
                f"Ollama response missing 'response' field; raw={response.text[:200]}"
            ) from exc

        return LLMResult(text=text.strip(), provider=self.name, model=model)

    def generate_stream(self, prompt: str, model: str | None = None):
        selected_model = model or settings.OLLAMA_ANSWER_MODEL
        payload = {
            "model": selected_model,
            "prompt": prompt,
            "stream": True,
        }

        with requests.post(
            settings.OLLAMA_URL,
            json=payload,
            timeout=settings.LLM_TIMEOUT_SECONDS,
            stream=True,
        ) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if not line:
                    continue
                chunk = json.loads(line)
                token = chunk.get("response", "")
                if token:
                    yield token
                if chunk.get("done"):
                    break
