"""
LLM-as-Judge for Ask endpoint evaluation.

Uses Gemini with schema-enforced JSON output to score answer quality.
Produces structured JudgeScores for each (question, context, answer) triple.

Design principles
-----------------
- Strict rubric: no partial credit ambiguity in the prompt.
- Deterministic: temperature=0, responseSchema enforced by the API.
- Fault-tolerant: JSON repair fallback before raising JudgeError.
- Cost-aware: uses the same model as answer generation (gemini-2.0-flash).
"""

from __future__ import annotations

import json
import logging
import re

from app.core.config import settings
from app.evaluation.ask.models import JudgeScores
from app.services.llm_providers import LLMProviderError


logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Gemini pricing constants (USD per 1M tokens, as of 2025)
# gemini-2.0-flash: $0.075/M input, $0.30/M output
# ---------------------------------------------------------------------------
GEMINI_FLASH_INPUT_COST_PER_M  = 0.075
GEMINI_FLASH_OUTPUT_COST_PER_M = 0.300


class JudgeError(RuntimeError):
    """Raised when the judge cannot produce a valid evaluation."""


# ---------------------------------------------------------------------------
# Judge prompt
# ---------------------------------------------------------------------------

_JUDGE_PROMPT_TEMPLATE = """\
You are a precise evaluation judge for a RAG (Retrieval-Augmented Generation) system.

Your task is to score the quality of a generated answer given:
1. The original question
2. The retrieved context chunks (the ONLY information the model was given)
3. The generated answer
4. The reference answer (optional — if provided, use it for correctness scoring)

QUESTION:
{question}

RETRIEVED CONTEXT:
{context}

GENERATED ANSWER:
{answer}

REFERENCE ANSWER:
{reference_answer}

Score each dimension from 0.0 to 1.0. Use the FULL range — do not cluster around 0.5.

Definitions (apply strictly):
- correctness: Does the answer correctly address the question? Compare to the reference answer if one is provided. 1.0 = fully correct and complete. 0.0 = wrong, off-topic, or directly contradicts the reference.
- groundedness: Are ALL factual claims in the answer traceable to the retrieved context? 1.0 = every claim is in context. 0.0 = all claims are unsupported.
- faithfulness: Does the answer avoid contradicting the retrieved context? 1.0 = no contradictions. 0.0 = directly contradicts retrieved information.
- hallucination: Did the model invent facts not present in the context? 1.0 = no hallucination. 0.0 = answer is almost entirely invented.
- completeness: Did the answer include the key information available in the retrieved context that is relevant to the question? 1.0 = all key points addressed. 0.0 = critical information is missing.
- overall: Your holistic assessment of the answer quality from a user's perspective.

Special rules:
- If the answer is exactly "I could not find that information in your notes." — set correctness=1.0 if and only if the context does not contain enough information to answer the question. Set groundedness=1.0 and hallucination=1.0.
- If the retrieved context is empty — set groundedness=0.0 and hallucination=0.0 (cannot be assessed).
- Do NOT give a claim partial credit. Either it is fully grounded or it is not.
- A correct answer that adds unretrieved background facts still loses groundedness points.

Respond with ONLY valid JSON. No markdown fences. No preamble. No explanation outside the JSON.

Required schema:
{{
  "correctness": <float 0.0-1.0>,
  "groundedness": <float 0.0-1.0>,
  "faithfulness": <float 0.0-1.0>,
  "hallucination": <float 0.0-1.0>,
  "completeness": <float 0.0-1.0>,
  "overall": <float 0.0-1.0>,
  "justification": "<2-3 concise sentences explaining your scores>",
  "hallucinated_claims": ["<exact claim text>"],
  "ungrounded_claims": ["<exact claim text>"]
}}
"""


# ---------------------------------------------------------------------------
# Gemini response schema (used with responseMimeType=application/json)
# ---------------------------------------------------------------------------

_JUDGE_RESPONSE_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "correctness":         {"type": "NUMBER"},
        "groundedness":        {"type": "NUMBER"},
        "faithfulness":        {"type": "NUMBER"},
        "hallucination":       {"type": "NUMBER"},
        "completeness":        {"type": "NUMBER"},
        "overall":             {"type": "NUMBER"},
        "justification":       {"type": "STRING"},
        "hallucinated_claims": {"type": "ARRAY", "items": {"type": "STRING"}},
        "ungrounded_claims":   {"type": "ARRAY", "items": {"type": "STRING"}},
    },
    "required": [
        "correctness", "groundedness", "faithfulness",
        "hallucination", "completeness", "overall",
        "justification", "hallucinated_claims", "ungrounded_claims",
    ],
}


# ---------------------------------------------------------------------------
# JSON repair helpers (mirrored from llm_service to avoid circular imports)
# ---------------------------------------------------------------------------

def _strip_fences(text: str) -> str:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned.strip()


def _try_repair(text: str) -> dict | None:
    cleaned = _strip_fences(text)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass
    return None


# ---------------------------------------------------------------------------
# AskJudge
# ---------------------------------------------------------------------------

class AskJudge:
    """
    Evaluates a single (question, context, answer) triple using Gemini.

    The judge uses schema-enforced JSON output (temperature=0) to produce
    deterministic, structured scores.
    """

    def __init__(self) -> None:
        if not settings.GEMINI_API_KEY:
            raise JudgeError("GEMINI_API_KEY is not configured — judge cannot run")

    def evaluate(
        self,
        question: str,
        context: str,
        answer: str,
        reference_answer: str = "",
    ) -> JudgeScores:
        """
        Score one answer.

        Parameters
        ----------
        question         The question sent to the Ask endpoint.
        context          The formatted context string (as built by AskService._build_context).
        answer           The answer generated by the Ask endpoint.
        reference_answer Optional reference answer for correctness comparison.

        Returns
        -------
        JudgeScores with all metrics populated.

        Raises
        ------
        JudgeError if Gemini fails or returns unrecoverable JSON after repair.
        """
        prompt = _JUDGE_PROMPT_TEMPLATE.format(
            question=question,
            context=context or "(no context retrieved)",
            answer=answer,
            reference_answer=reference_answer or "(no reference answer provided)",
        )

        raw = self._call_gemini(prompt)
        data = _try_repair(raw)
        if data is None:
            raise JudgeError(
                f"Judge returned unrecoverable JSON after repair. raw={raw[:200]!r}"
            )

        try:
            return JudgeScores(**self._coerce_scores(data))
        except Exception as exc:
            raise JudgeError(f"JudgeScores validation failed: {exc}. data={data}") from exc

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _call_gemini(self, prompt: str) -> str:
        import requests  # local import — judge is evaluation-only code
        import time

        url = (
            f"{settings.GEMINI_API_BASE}/models/{settings.GEMINI_ANSWER_MODEL}"
            f":generateContent?key={settings.GEMINI_API_KEY}"
        )
        payload = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0,
                "responseMimeType": "application/json",
                "responseSchema": _JUDGE_RESPONSE_SCHEMA,
            },
        }

        max_retries = 5
        backoff = 2.0
        for attempt in range(max_retries):
            try:
                resp = requests.post(url, json=payload, timeout=settings.LLM_TIMEOUT_SECONDS)
                if resp.status_code == 429:
                    logger.warning(
                        "Judge Gemini returned 429 (Rate Limit). Retrying in %.1fs... (attempt %d/%d)",
                        backoff,
                        attempt + 1,
                        max_retries,
                    )
                    time.sleep(backoff)
                    backoff *= 2.0
                    continue
                resp.raise_for_status()
                break
            except requests.exceptions.Timeout:
                raise JudgeError(
                    f"Judge Gemini call timed out after {settings.LLM_TIMEOUT_SECONDS}s"
                )
            except requests.RequestException as exc:
                if attempt == max_retries - 1:
                    raise JudgeError(f"Judge Gemini HTTP error after retries: {exc}") from exc
                time.sleep(backoff)
                backoff *= 2.0
        else:
            raise JudgeError(
                f"Judge Gemini failed after {max_retries} retries due to rate limiting (429)"
            )

        data = resp.json()
        try:
            text = data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError, TypeError) as exc:
            raise JudgeError(
                f"Judge Gemini response missing text; raw={str(data)[:300]}"
            ) from exc

        logger.debug("Judge raw response: %.200s", text)
        return text.strip()

    @staticmethod
    def _coerce_scores(data: dict) -> dict:
        """
        Clamp all numeric scores to [0.0, 1.0] and ensure list fields exist.
        Protects downstream Pydantic validation from out-of-range values.
        """
        score_fields = [
            "correctness", "groundedness", "faithfulness",
            "hallucination", "completeness", "overall",
        ]
        for field in score_fields:
            if field in data:
                try:
                    data[field] = max(0.0, min(1.0, float(data[field])))
                except (TypeError, ValueError):
                    data[field] = 0.0
            else:
                data[field] = 0.0

        data.setdefault("justification", "")
        data.setdefault("hallucinated_claims", [])
        data.setdefault("ungrounded_claims", [])
        return data


# ---------------------------------------------------------------------------
# Cost estimation
# ---------------------------------------------------------------------------

def estimate_tokens(text: str) -> int:
    """Rough token estimate: 4 characters per token (heuristic)."""
    return max(1, len(text) // 4)


def estimate_cost_usd(prompt_tokens: int, completion_tokens: int) -> float:
    """
    Estimate Gemini 2.0 Flash cost in USD.

    Pricing: $0.075 per 1M input tokens, $0.30 per 1M output tokens.
    """
    input_cost  = (prompt_tokens  / 1_000_000) * GEMINI_FLASH_INPUT_COST_PER_M
    output_cost = (completion_tokens / 1_000_000) * GEMINI_FLASH_OUTPUT_COST_PER_M
    return round(input_cost + output_cost, 8)
