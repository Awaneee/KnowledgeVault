"""
LLM service — provider-agnostic gateway with intelligent failover.

Two separate provider chains:
  - Intent extraction:  Gemini → rule-based fallback (Groq excluded by design)
  - Answer generation:  priority list from LLM_PROVIDER_PRIORITY env var

Failover behaviour:
  - Gemini: attempt → JSON repair (intent only) → retry once → move to next
  - Any provider: 429 / quota / timeout / 5xx → move to next, log reason
  - Ollama: only in chain when OLLAMA_ENABLED=true
  - Exhausted: raises AllProvidersExhausted (callers handle graceful degradation)

Provider metrics are recorded via llm_metrics.metrics for every attempt.
"""

import json
import logging
import re
import time

from app.core.config import settings
from app.services.llm_metrics import metrics
from app.services.llm_providers import GeminiProvider
from app.services.llm_providers import GroqProvider
from app.services.llm_providers import LLMProvider
from app.services.llm_providers import LLMProviderError
from app.services.llm_providers import LLMResult
from app.services.llm_providers import OllamaProvider
from app.services.llm_providers import OpenRouterProvider


logger = logging.getLogger(__name__)


class AllProvidersExhausted(LLMProviderError):
    """
    Raised when every provider in the chain has failed.

    Callers (e.g. AskService) must catch this and return a
    graceful retrieval-only response rather than propagating a 500.
    """


# ---------------------------------------------------------------------------
# JSON helpers
# ---------------------------------------------------------------------------

def _strip_markdown_fences(text: str) -> str:
    """Remove leading/trailing markdown code fences from LLM output."""
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned.strip()


def _try_repair_json(text: str) -> str | None:
    """
    Attempt to extract a JSON object from malformed LLM output.
    Returns the repaired JSON string, or None if unrecoverable.
    """
    cleaned = _strip_markdown_fences(text)
    # Try direct parse first.
    try:
        json.loads(cleaned)
        return cleaned
    except json.JSONDecodeError:
        pass
    # Find the first '{...}' block.
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if match:
        candidate = match.group(0)
        try:
            json.loads(candidate)
            return candidate
        except json.JSONDecodeError:
            pass
    return None


def is_valid_intent_json(text: str) -> bool:
    """Return True if text is valid intent JSON with required keys."""
    repaired = _try_repair_json(text)
    if not repaired:
        return False
    try:
        data = json.loads(repaired)
        return isinstance(data, dict) and "intent_type" in data and "confidence" in data
    except Exception:
        return False


def classify_llm_exception(exc: Exception) -> str:
    """Classify an exception into a human-readable failure reason."""
    err_msg = str(exc).lower()
    if "timeout" in err_msg:
        return "timeout"
    if "429" in err_msg or "quota" in err_msg or "rate limit" in err_msg:
        return "quota_exceeded"
    if any(code in err_msg for code in ("503", "500", "502", "504")):
        return "api_5xx"
    if "unavailable" in err_msg or "connection" in err_msg:
        return "api_unavailable"
    if "non-json" in err_msg or "missing text" in err_msg or "missing content" in err_msg:
        return "malformed_response"
    return "unknown_error"


# ---------------------------------------------------------------------------
# LLMService
# ---------------------------------------------------------------------------

class LLMService:
    """
    Provider-agnostic LLM gateway.

    Intent extraction and answer generation use separate provider chains
    because intent extraction requires schema-enforced JSON (Gemini only),
    while answer generation can safely fall through to Groq and Ollama.
    """

    @classmethod
    def extract_intent(cls, prompt: str) -> LLMResult:
        """
        Structured intent extraction.

        Chain: Gemini (with JSON repair + one retry) → AllProvidersExhausted.
        Callers catch AllProvidersExhausted and invoke the rule-based extractor.
        Ollama is not used here because it cannot guarantee schema compliance.
        """
        provider = cls._try_build_provider("gemini")
        if provider is None:
            raise AllProvidersExhausted("Gemini unavailable and no intent fallback configured")

        errors: list[str] = []

        # Attempt 1.
        try:
            t0 = time.monotonic()
            with metrics.track("gemini", "intent"):
                result = provider.extract_intent(prompt)
            logger.info(
                "LLM intent provider=gemini latency=%.2fs",
                time.monotonic() - t0,
            )
            if is_valid_intent_json(result.text):
                return result
            logger.warning("Gemini intent JSON invalid — attempting JSON repair")
            repaired = _try_repair_json(result.text)
            if repaired and is_valid_intent_json(repaired):
                logger.info("Gemini intent JSON repaired successfully")
                return LLMResult(
                    text=repaired,
                    provider=result.provider,
                    model=result.model,
                    fallback_events=("json_repaired",),
                )
        except Exception as exc:
            reason = classify_llm_exception(exc)
            errors.append(f"gemini attempt-1: {reason}: {exc}")
            logger.warning("LLM intent gemini attempt-1 failed reason=%s", reason)

        # Attempt 2 — retry once.
        try:
            t0 = time.monotonic()
            with metrics.track("gemini", "intent_retry"):
                result = provider.extract_intent(prompt)
            logger.info(
                "LLM intent provider=gemini retry latency=%.2fs",
                time.monotonic() - t0,
            )
            if is_valid_intent_json(result.text):
                return LLMResult(
                    text=result.text,
                    provider=result.provider,
                    model=result.model,
                    fallback_events=("retried",),
                )
            logger.warning("Gemini intent JSON invalid after retry — falling back to rules")
        except Exception as exc:
            reason = classify_llm_exception(exc)
            errors.append(f"gemini attempt-2: {reason}: {exc}")
            logger.warning("LLM intent gemini attempt-2 failed reason=%s", reason)

        raise AllProvidersExhausted("; ".join(errors) or "Gemini returned invalid JSON twice")

    @classmethod
    def generate(
        cls,
        prompt: str,
        model: str | None = None,
    ) -> str:
        """
        Free-form text generation (answer, title).
        Returns the raw text string for backward compatibility.
        Raises AllProvidersExhausted if every provider fails.
        """
        result = cls._run_answer_with_fallback(prompt=prompt, model=model)
        return result.text

    @classmethod
    def generate_stream(cls, prompt: str, model: str | None = None):
        """
        Streaming token generator.

        Iterates the answer provider chain. If a provider fails mid-stream
        after yielding tokens, the stream ends cleanly rather than raising.
        """
        providers = cls._answer_provider_chain()
        errors: list[str] = []

        for index, provider in enumerate(providers):
            try:
                logger.info("LLM stream attempt provider=%s", provider.name)
                t0 = time.monotonic()
                token_count = 0
                for token in provider.generate_stream(prompt=prompt, model=model):
                    token_count += 1
                    yield token
                logger.info(
                    "LLM stream complete provider=%s tokens=%d latency=%.2fs",
                    provider.name,
                    token_count,
                    time.monotonic() - t0,
                )
                return
            except Exception as exc:
                reason = classify_llm_exception(exc)
                errors.append(f"{provider.name}: {reason}")
                logger.warning(
                    "LLM stream provider=%s failed reason=%s",
                    provider.name,
                    reason,
                )
                if index < len(providers) - 1:
                    next_name = providers[index + 1].name
                    metrics.record_fallback(provider.name, next_name, reason)
                    logger.warning(
                        "LLM stream falling back from %s → %s",
                        provider.name,
                        next_name,
                    )

        logger.error("LLM stream all providers failed errors=%s", errors)
        raise AllProvidersExhausted("; ".join(errors))

    # ------------------------------------------------------------------
    # Internal — answer generation fallback chain
    # ------------------------------------------------------------------

    @classmethod
    def _run_answer_with_fallback(
        cls,
        prompt: str,
        model: str | None = None,
    ) -> LLMResult:
        providers = cls._answer_provider_chain()
        errors: list[str] = []

        for index, provider in enumerate(providers):
            try:
                t0 = time.monotonic()
                logger.info(
                    "LLM answer attempt provider=%s",
                    provider.name,
                )
                with metrics.track(provider.name, "answer"):
                    result = provider.generate_answer(prompt=prompt, model=model)
                elapsed = time.monotonic() - t0
                logger.info(
                    "LLM answer success provider=%s model=%s latency=%.2fs",
                    result.provider,
                    result.model,
                    elapsed,
                )
                if errors:
                    logger.warning(
                        "LLM answer fallback succeeded provider=%s after=%s",
                        provider.name,
                        errors,
                    )
                    return LLMResult(
                        text=result.text,
                        provider=result.provider,
                        model=result.model,
                        fallback_events=tuple(errors),
                    )
                return result

            except Exception as exc:
                reason = classify_llm_exception(exc)
                message = f"{provider.name}: {reason}: {exc}"
                errors.append(message)
                logger.warning("LLM answer provider=%s failed reason=%s", provider.name, reason)

                if index < len(providers) - 1:
                    next_name = providers[index + 1].name
                    metrics.record_fallback(provider.name, next_name, reason)
                    logger.warning(
                        "LLM answer falling back %s → %s",
                        provider.name,
                        next_name,
                    )

        raise AllProvidersExhausted("; ".join(errors) or "No answer providers configured")

    @classmethod
    def _answer_provider_chain(cls) -> list[LLMProvider]:
        """
        Build the ordered provider list for answer generation.

        Reads LLM_PROVIDER_PRIORITY (comma-separated). Falls back to
        LLM_PROVIDER for backward compatibility. Ollama is only included
        when OLLAMA_ENABLED=true.
        """
        priority_str = (
            settings.LLM_PROVIDER_PRIORITY
            or settings.LLM_PROVIDER
            or "gemini,groq"
        ).strip()
        names = [n.strip().lower() for n in priority_str.split(",") if n.strip()]

        chain: list[LLMProvider] = []
        for name in names:
            provider = cls._try_build_provider(name)
            if provider is not None:
                chain.append(provider)

        if not chain:
            logger.error("LLM answer chain is empty — no providers are configured")

        return chain

    @classmethod
    def _try_build_provider(cls, name: str) -> LLMProvider | None:
        """Attempt to instantiate a provider; return None on misconfiguration."""
        try:
            if name == "gemini":
                return GeminiProvider()
            if name == "groq":
                return GroqProvider()
            if name == "openrouter":
                return OpenRouterProvider()
            if name == "ollama":
                if not settings.OLLAMA_ENABLED:
                    logger.debug(
                        "LLM provider=ollama skipped — OLLAMA_ENABLED is false"
                    )
                    return None
                return OllamaProvider()
            logger.warning("LLM unknown provider name=%s — skipping", name)
            return None
        except LLMProviderError as exc:
            logger.warning("LLM provider=%s unavailable: %s", name, exc)
            return None
