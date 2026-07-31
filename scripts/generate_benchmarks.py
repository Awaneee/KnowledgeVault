"""
Benchmark generator — five-stage pipeline.

Produces two output files:
  - benchmark/candidates.json  (auto-generated, needs human review)
  - benchmark/verified.json    (human-reviewed; created by human_eval.py)

Stage 1 — Corpus sampling
    Keyword-based candidate generation using topic clusters from the note
    corpus.  Optional LLM-based query generation with --llm-queries.

Stage 2 — Retrieval-based relevance expansion
    Runs retrieve_hybrid() on each candidate query and adds retrieved notes
    that pass a similarity threshold to the relevant set.
    Requires a running database. Enabled with --expand-relevance.

Stage 3 — Embedding deduplication
    Removes near-duplicate queries (cosine similarity > 0.90 between
    all-MiniLM-L6-v2 query embeddings). Enabled with --dedup.

Stage 4 — Quality filter
    Removes entries with: no relevant notes, query < 3 tokens,
    all relevant notes in singleton categories.

Stage 5 — Export
    Writes candidates.json with stable IDs and benchmark/manifest.json.

Stable ID format:  {note_id}_{query_type}_{sha256_prefix}
  where query_type ∈ {"kw", "nl", "tp"} (keyword / natural-language / template)
  and sha256_prefix is the first 6 chars of SHA256(query_text).

Usage:
    # Fast run — keyword templates only, no DB, no dedup:
    python scripts/generate_benchmarks.py \\
        --user-id 1 --output-dir app/evaluation/benchmark

    # Full pipeline with retrieval expansion and deduplication:
    python scripts/generate_benchmarks.py \\
        --user-id 1 --output-dir app/evaluation/benchmark \\
        --expand-relevance --dedup

    # With LLM query generation (requires GEMINI_API_KEY):
    python scripts/generate_benchmarks.py \\
        --user-id 1 --output-dir app/evaluation/benchmark \\
        --llm-queries --expand-relevance --dedup
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import sys
from pathlib import Path
from typing import NamedTuple

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import app.database.base_all  # noqa: F401
from app.database.session import SessionLocal
from app.models.notes import Note
from sqlalchemy.orm import Session

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("generate_benchmarks")


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

class NoteRecord(NamedTuple):
    id: int
    title: str
    content: str


class CandidateEntry:
    """A candidate benchmark query before human review."""

    def __init__(
        self,
        primary_note_id: int,
        query: str,
        query_type: str,  # "kw" | "nl" | "tp" | "llm_kw" | "llm_nl"
        relevant_note_ids: list[int],
        expected_intent: str,
        expected_category: str,
        difficulty: str,
        tags: list[str],
        retrieval_challenge: str | None = None,
    ):
        self.primary_note_id = primary_note_id
        self.query = query
        self.query_type = query_type
        self.relevant_note_ids = relevant_note_ids
        self.expected_intent = expected_intent
        self.expected_category = expected_category
        self.difficulty = difficulty
        self.tags = tags
        self.retrieval_challenge = retrieval_challenge
        self.id = self._make_id()

    def _make_id(self) -> str:
        digest = hashlib.sha256(self.query.encode()).hexdigest()[:6]
        return f"{self.primary_note_id}_{self.query_type}_{digest}"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "query": self.query,
            "expected_intent": self.expected_intent,
            "expected_category": self.expected_category,
            "relevant_note_ids": self.relevant_note_ids,
            "difficulty": self.difficulty,
            "tags": self.tags,
            "retrieval_challenge": self.retrieval_challenge,
            "graded_relevance": None,  # to be filled by human_eval.py
            "labeling_notes": "",
            "labeled_at": None,
        }


# ---------------------------------------------------------------------------
# Stage 1 helpers — corpus keyword matching
# ---------------------------------------------------------------------------

def load_notes(db: Session, user_id: int) -> list[NoteRecord]:
    rows = (
        db.query(Note.id, Note.title, Note.content)
        .filter(Note.user_id == user_id, Note.organization_status == "organized")
        .order_by(Note.id)
        .all()
    )
    return [NoteRecord(r.id, r.title or "", r.content or "") for r in rows]


def find_notes(notes: list[NoteRecord], *keywords: str, min_match: int = 1) -> list[int]:
    kws = [k.lower() for k in keywords]
    matched = []
    for n in notes:
        text = (n.title + " " + n.content).lower()
        if sum(1 for k in kws if k in text) >= min_match:
            matched.append(n.id)
    return matched


def find_notes_exact(notes: list[NoteRecord], phrase: str) -> list[int]:
    pl = phrase.lower()
    return [n.id for n in notes if pl in (n.title + " " + n.content).lower()]


def _e(
    primary_id: int,
    query: str,
    ids: list[int],
    intent: str,
    category: str,
    difficulty: str = "medium",
    tags: list[str] | None = None,
    retrieval_challenge: str | None = None,
    query_type: str = "tp",
) -> CandidateEntry | None:
    """Shorthand constructor — returns None if ids is empty."""
    if not ids:
        return None
    primary = primary_id if primary_id in ids else (ids[0] if ids else 0)
    return CandidateEntry(
        primary_note_id=primary,
        query=query,
        query_type=query_type,
        relevant_note_ids=ids[:10],
        expected_intent=intent,
        expected_category=category,
        difficulty=difficulty,
        tags=tags or [],
        retrieval_challenge=retrieval_challenge,
    )


# ---------------------------------------------------------------------------
# Stage 1 — Template-based candidate generation
# ---------------------------------------------------------------------------

def stage1_template_candidates(notes: list[NoteRecord]) -> list[CandidateEntry]:
    """Generate keyword-template candidates.  This replaces the former monolithic
    generate_retrieval_benchmark() function with a structured 5-stage pipeline."""
    entries: list[CandidateEntry | None] = []

    def add(primary_id: int, query: str, ids: list[int], intent: str,
            category: str, difficulty: str = "medium",
            tags: list[str] | None = None,
            challenge: str | None = None,
            qtype: str = "tp") -> None:
        entries.append(_e(primary_id, query, ids, intent, category, difficulty, tags, challenge, qtype))

    # ── Programming ──
    py_ids = find_notes(notes, "python", min_match=1)[:8]
    if py_ids:
        add(py_ids[0], "What are useful Python tips and tricks I've learned?", py_ids, "study", "Study - Python", "easy", ["python"], "semantic")
        add(py_ids[0], "Show my Python programming notes", py_ids, "study", "Study - Python", "easy", ["python"], "lexical")

    async_ids = find_notes(notes, "async", "asyncio", "coroutine", min_match=1)
    if async_ids:
        add(async_ids[0], "How does Python async programming work?", async_ids, "study", "Study - Python", "medium", ["python", "async"], "semantic")

    git_ids = find_notes(notes, "git", "branch", "commit", "rebase", min_match=1)
    if git_ids:
        add(git_ids[0], "What git commands and workflows have I noted?", git_ids, "reference", "Reference - Git", "easy", ["git"], "semantic")
        add(git_ids[0], "Git tips and tricks", git_ids, "reference", "Reference - Git", "easy", ["git"], "lexical")

    # ── AI / ML ──
    rag_ids = find_notes(notes, "rag", "retrieval-augmented", "retrieval augmented", min_match=1)
    if rag_ids:
        add(rag_ids[0], "What do I know about RAG systems?", rag_ids, "study", "Study - AI", "medium", ["rag", "ai"], "semantic")
        add(rag_ids[0], "Retrieval augmented generation notes", rag_ids, "study", "Study - AI", "easy", ["rag"], "lexical")

    embed_ids = find_notes(notes, "embedding", "vector", "semantic", "cosine", min_match=2)
    if embed_ids:
        add(embed_ids[0], "Notes about embeddings and vector search", embed_ids, "study", "Study - AI", "medium", ["embeddings", "vectors"], "semantic")

    llm_ids = find_notes(notes, "llm", "language model", "gpt", "gemini", "groq", min_match=1)
    if llm_ids:
        add(llm_ids[0], "Large language model notes and findings", llm_ids, "study", "Study - AI", "medium", ["llm", "ai"], "semantic")

    rerank_ids = find_notes(notes, "rerank", "cross-encoder", "reranker", "bi-encoder", min_match=1)
    if rerank_ids:
        add(rerank_ids[0], "Notes about reranking in search systems", rerank_ids, "study", "Study - AI", "hard", ["reranking", "search"], "semantic")

    eval_ids = find_notes(notes, "evaluation", "benchmark", "metrics", "mrr", "recall", "ndcg", "precision", min_match=2)
    if eval_ids:
        add(eval_ids[0], "RAG and retrieval evaluation metrics", eval_ids, "study", "Study - AI", "hard", ["evaluation", "metrics"], "multi_hop")
        add(eval_ids[0], "How do I measure retrieval quality?", eval_ids, "study", "Study - AI", "hard", ["evaluation"], "semantic")

    prompt_ids = find_notes(notes, "prompt", "few-shot", "zero-shot", "chain-of-thought", "temperature", min_match=1)
    if prompt_ids:
        add(prompt_ids[0], "Prompting techniques and tips", prompt_ids, "study", "Study - AI", "medium", ["prompting"], "semantic")

    # ── System Design ──
    cache_ids = find_notes(notes, "cache", "redis cache", "eviction", "lru", "bloom filter", min_match=1)
    if cache_ids:
        add(cache_ids[0], "Caching strategies and implementations", cache_ids, "study", "Study - System Design", "medium", ["caching"], "semantic")

    queue_ids = find_notes(notes, "kafka", "message queue", "rabbitmq", "event", "producer", "consumer", min_match=1)
    if queue_ids:
        add(queue_ids[0], "Message queue and event streaming notes", queue_ids, "study", "Study - System Design", "medium", ["kafka", "queues"], "semantic")

    sysdesign_ids = find_notes(notes, "system design", "url shortener", "twitter", "rate limiter", "consistent hashing", min_match=1)
    if sysdesign_ids:
        add(sysdesign_ids[0], "System design interview prep notes", sysdesign_ids, "study", "Study - System Design", "medium", ["system_design", "interview"], "semantic")

    # ── Database ──
    postgres_ids = find_notes(notes, "postgresql", "postgres", "pgvector", "explain analyze", min_match=1)
    if postgres_ids:
        add(postgres_ids[0], "PostgreSQL database notes", postgres_ids, "study", "Study - PostgreSQL", "medium", ["postgresql"], "lexical")

    redis_ids = find_notes(notes, "redis", "cache", "queue", "pubsub", min_match=1)
    if redis_ids:
        add(redis_ids[0], "Redis usage and patterns", redis_ids, "study", "Study - Redis", "easy", ["redis"], "lexical")

    docker_ids = find_notes(notes, "docker", "container", "compose", "dockerfile", min_match=1)
    if docker_ids:
        add(docker_ids[0], "Docker and containerization notes", docker_ids, "study", "Study - Docker", "easy", ["docker"], "lexical")
        add(docker_ids[0], "What Docker tips have I collected?", docker_ids, "reference", "Reference - Docker", "easy", ["docker"], "semantic")

    fastapi_ids = find_notes(notes, "fastapi", "dependency injection", "router", "pydantic", min_match=1)
    if fastapi_ids:
        add(fastapi_ids[0], "FastAPI development notes", fastapi_ids, "study", "Study - FastAPI", "medium", ["fastapi"], "lexical")

    # ── Projects ──
    kv_ids = find_notes(notes, "knowledgevault", "knowledge vault", "kv", min_match=1)
    if kv_ids:
        add(kv_ids[0], "KnowledgeVault project notes", kv_ids, "reference", "Reference - KnowledgeVault", "easy", ["project"], "lexical")
        add(kv_ids[0], "What decisions have I made for the KnowledgeVault project?", kv_ids, "reference", "Reference - KnowledgeVault", "medium", ["project", "architecture"], "multi_hop")

    # ── Meetings ──
    meeting_ids = find_notes(notes, "meeting", "sync", "standup", "sprint", "retrospective", min_match=1)
    if meeting_ids:
        add(meeting_ids[0], "What meetings have I had?", meeting_ids, "event", "Meetings", "easy", ["meetings"], "semantic")

    # ── Reminders / Tasks ──
    todo_ids = find_notes(notes, "deadline", "submit", "due", "complete", min_match=2)
    if todo_ids:
        add(todo_ids[0], "What are my pending tasks and deadlines?", todo_ids[:6], "todo", "Tasks", "easy", ["todo", "deadlines"], "semantic")

    appointment_ids = find_notes(notes, "appointment", "dentist", "doctor", "checkup", "health", min_match=1)
    if appointment_ids:
        add(appointment_ids[0], "What health appointments do I have?", appointment_ids, "reminder", "Appointments", "easy", ["appointments", "health"], "semantic")

    payment_ids = find_notes(notes, "pay", "bill", "fee", "rent", "electricity", min_match=1)
    if payment_ids:
        add(payment_ids[0], "What payments and bills do I need to make?", payment_ids, "todo", "Bills", "easy", ["bills", "finance"], "semantic")

    grocery_ids = find_notes(notes, "grocery", "groceries", "milk", "eggs", "bread", "buy", min_match=2)
    if grocery_ids:
        add(grocery_ids[0], "What is on my shopping list?", grocery_ids, "todo", "Shopping", "easy", ["shopping", "grocery"], "lexical")

    remind_ids = find_notes(notes, "remind", "reminder", "don't forget", "remember", min_match=1)
    if remind_ids:
        add(remind_ids[0], "Show all my reminders", remind_ids[:8], "reminder", "Reminders", "easy", ["reminders"], "semantic")

    # ── Finance / Budget ──
    budget_ids = find_notes(notes, "budget", "spending", "expense", "monthly", "tracking", min_match=1)
    if budget_ids:
        add(budget_ids[0], "My budget and expense tracking notes", budget_ids, "todo", "Finance", "easy", ["budget", "finance"], "semantic")

    # ── Travel ──
    travel_ids = find_notes(notes, "trip", "travel", "train", "flight", "hotel", "itinerary", min_match=1)
    if travel_ids:
        add(travel_ids[0], "My travel plans and notes", travel_ids, "todo", "Travel", "easy", ["travel"], "semantic")

    # ── Health ──
    workout_ids = find_notes(notes, "workout", "exercise", "gym", "fitness", "push", min_match=1)
    if workout_ids:
        add(workout_ids[0], "Fitness and workout notes", workout_ids, "todo", "Health", "easy", ["fitness", "workout"], "semantic")

    # ── Startups / Ideas ──
    startup_ids = find_notes(notes, "startup", "business", "product", "market", "idea", "saas", min_match=1)
    if startup_ids:
        add(startup_ids[0], "My startup ideas and business notes", startup_ids, "idea", "Ideas - Startups", "easy", ["startup"], "semantic")
        add(startup_ids[0], "What business ideas have I documented?", startup_ids, "idea", "Ideas", "easy", ["startup", "ideas"], "semantic")

    # ── Communication ──
    sid_ids = find_notes(notes, "sid", "siddhant", min_match=1)
    if sid_ids:
        add(sid_ids[0], "Things I need to tell Sid", sid_ids, "communication", "Things to Tell Sid", "easy", ["sid"], "lexical")
        add(sid_ids[0], "Things to discuss with Sid at the next meeting", sid_ids, "communication", "Things to Tell Sid", "easy", ["sid"], "semantic")
        add(sid_ids[0], "Message to send to Siddhant about backend", sid_ids, "communication", "Things to Tell Sid", "medium", ["siddhant", "backend"], "lexical_gap")

    # ── Exact phrase queries ──
    bm25_ids = find_notes_exact(notes, "BM25")
    if bm25_ids:
        add(bm25_ids[0], "BM25", bm25_ids, "study", "Study - AI", "easy", ["bm25", "exact"], "exact_phrase")

    hnsw_ids = find_notes_exact(notes, "HNSW")
    if hnsw_ids:
        add(hnsw_ids[0], "HNSW index", hnsw_ids, "study", "Study - AI", "easy", ["hnsw", "exact"], "exact_phrase")

    rrf_ids = find_notes_exact(notes, "Reciprocal Rank Fusion")
    if rrf_ids:
        add(rrf_ids[0], "Reciprocal Rank Fusion", rrf_ids, "study", "Study - AI", "medium", ["rrf", "exact"], "exact_phrase")

    cap_ids = find_notes_exact(notes, "CAP theorem")
    if cap_ids:
        add(cap_ids[0], "CAP theorem", cap_ids, "study", "Study - System Design", "easy", ["cap", "exact"], "exact_phrase")

    # ── Comparison queries ──
    if redis_ids and queue_ids:
        redis_kafka_ids = list(set(redis_ids) | set(queue_ids))
        add(redis_ids[0], "Redis vs Kafka — when to use each", redis_kafka_ids[:6], "study", "Study - System Design", "hard", ["comparison", "redis", "kafka"], "comparison")

    if py_ids and fastapi_ids:
        backend_ids = list(set(py_ids[:4]) | set(fastapi_ids[:4]))
        add(py_ids[0], "Resources for learning backend development", backend_ids[:8], "study", "Study - Backend", "medium", ["backend", "learning"], "semantic")

    # ── Negative queries (no relevant notes expected) ──
    # These test RETRIEVAL_MIN_SCORE filtering.
    # The benchmark marks them with retrieval_challenge="negative" and an empty relevant set.
    # They are excluded from Recall/Precision scoring but test that the system
    # correctly returns no results (or filters below the score threshold).
    no_notes = []  # deliberately empty relevant set
    # We still emit them so human_eval.py can confirm they're negative.
    def add_negative(query: str, tags: list[str]) -> None:
        entry = CandidateEntry(
            primary_note_id=0,
            query=query,
            query_type="tp",
            relevant_note_ids=[],
            expected_intent="general",
            expected_category="General",
            difficulty="hard",
            tags=tags,
            retrieval_challenge="negative",
        )
        entries.append(entry)

    # Only add negative queries about topics not in the corpus
    # (these are safe to include regardless of corpus content)
    add_negative("Notes about Fortran programming", ["fortran", "negative"])
    add_negative("My notes on ancient Roman history", ["history", "negative"])
    add_negative("Cooking recipes I've saved", ["cooking", "negative"])

    # ── Multi-hop queries ──
    if kv_ids and rag_ids:
        kv_rag_ids = list(set(kv_ids) | set(rag_ids))
        add(kv_ids[0], "KnowledgeVault RAG pipeline decisions and findings", kv_rag_ids[:8], "reference", "Reference - KnowledgeVault", "hard", ["rag", "project"], "multi_hop")

    if eval_ids and kv_ids:
        eval_kv_ids = list(set(eval_ids) | set(kv_ids))
        add(kv_ids[0], "What benchmark results have I recorded for KnowledgeVault retrieval?", eval_kv_ids[:8], "reference", "Reference - KnowledgeVault", "hard", ["evaluation", "project"], "multi_hop")

    # ── Temporal queries ──
    feb_ids = find_notes(notes, "this week", "this month", "last week", "recently", min_match=1)
    if feb_ids:
        add(feb_ids[0], "What have I been working on this month?", feb_ids[:6], "general", "General", "hard", ["temporal"], "temporal")
        add(feb_ids[0], "Recent notes and activities", feb_ids[:6], "general", "General", "hard", ["temporal"], "temporal")

    # ── Synthesis queries ──
    ai_ids = list(set(llm_ids or []) | set(embed_ids or []) | set(rag_ids or []))
    if ai_ids:
        add(ai_ids[0] if ai_ids else 0, "My study notes on AI and machine learning", ai_ids[:8], "study", "Study - AI", "easy", ["study", "ai"], "synthesis")

    # Filter None entries
    return [e for e in entries if e is not None]


# ---------------------------------------------------------------------------
# Stage 2 — Retrieval-based relevance expansion
# ---------------------------------------------------------------------------

def stage2_expand_relevance(
    candidates: list[CandidateEntry],
    user_id: int,
    db: Session,
    similarity_threshold: float = 0.65,
) -> list[CandidateEntry]:
    """
    For each candidate, run retrieve_hybrid() and add retrieved notes that
    pass a similarity score threshold to the relevant set as grade-1 candidates.

    This produces a larger, retrieval-grounded relevant set that human
    reviewers can then trim down.
    """
    from app.services.chunk_service import ChunkService
    chunk_service = ChunkService(db)

    for entry in candidates:
        if entry.retrieval_challenge == "negative":
            continue  # don't expand negative queries

        try:
            results = chunk_service.retrieve_hybrid(
                query=entry.query,
                user_id=user_id,
                limit=20,
            )
            existing_ids = set(entry.relevant_note_ids)
            for r in results:
                score = r.get("score", 0.0)
                nid = r.get("note_id")
                if nid and nid not in existing_ids and score >= similarity_threshold:
                    entry.relevant_note_ids.append(nid)
                    existing_ids.add(nid)
        except Exception as exc:
            logger.warning("Retrieval expansion failed for %r: %s", entry.query, exc)

    return candidates


# ---------------------------------------------------------------------------
# Stage 3 — Embedding deduplication
# ---------------------------------------------------------------------------

def stage3_dedup(
    candidates: list[CandidateEntry],
    similarity_threshold: float = 0.90,
) -> list[CandidateEntry]:
    """
    Remove near-duplicate queries using all-MiniLM-L6-v2 embeddings.
    For pairs with cosine similarity > threshold, keep the one with more
    relevant notes (richer ground truth).
    """
    if not candidates:
        return candidates

    try:
        from app.core.embedding_model import embedding_model
        import numpy as np

        texts = [c.query for c in candidates]
        embeddings = embedding_model.encode(texts, normalize_embeddings=True)

        keep = [True] * len(candidates)
        for i in range(len(candidates)):
            if not keep[i]:
                continue
            for j in range(i + 1, len(candidates)):
                if not keep[j]:
                    continue
                sim = float(np.dot(embeddings[i], embeddings[j]))
                if sim > similarity_threshold:
                    # Keep the one with more relevant notes
                    if len(candidates[i].relevant_note_ids) >= len(candidates[j].relevant_note_ids):
                        keep[j] = False
                    else:
                        keep[i] = False
                        break  # i is now dropped, stop inner loop

        removed = sum(1 for k in keep if not k)
        logger.info("Stage 3 dedup: removed %d duplicates (%d remaining)", removed, sum(keep))
        return [c for c, k in zip(candidates, keep) if k]

    except Exception as exc:
        logger.warning("Stage 3 dedup skipped: %s", exc)
        return candidates


# ---------------------------------------------------------------------------
# Stage 4 — Quality filter
# ---------------------------------------------------------------------------

def stage4_quality_filter(candidates: list[CandidateEntry]) -> list[CandidateEntry]:
    """
    Remove entries that fail quality checks.
    Negative queries (retrieval_challenge="negative") bypass the relevance check.
    """
    kept: list[CandidateEntry] = []
    removed = 0
    for entry in candidates:
        # Must have ≥ 1 relevant note (unless it's a negative query)
        if entry.retrieval_challenge != "negative" and not entry.relevant_note_ids:
            removed += 1
            continue
        # Query must be ≥ 3 tokens
        if len(entry.query.split()) < 3:
            removed += 1
            continue
        kept.append(entry)

    logger.info("Stage 4 quality filter: removed %d, kept %d", removed, len(kept))
    return kept


# ---------------------------------------------------------------------------
# Stage 5 — Export
# ---------------------------------------------------------------------------

def stage5_export(
    candidates: list[CandidateEntry],
    output_dir: Path,
    note_count: int,
) -> None:
    """Write candidates.json and update benchmark/manifest.json."""
    entries = [c.to_dict() for c in candidates]

    candidates_path = output_dir / "candidates.json"
    candidates_path.write_text(json.dumps(entries, indent=2), encoding="utf-8")
    logger.info("Candidates written: %d entries → %s", len(entries), candidates_path)

    # Update manifest (don't overwrite verified.json info)
    manifest_path = output_dir / "manifest.json"
    manifest: dict = {}
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except Exception:
            pass
    manifest["candidate_count"] = len(entries)
    manifest["note_count_at_generation"] = note_count
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    logger.info("Manifest updated: %s", manifest_path)

    # Coverage report
    diff_counts: dict[str, int] = {}
    intent_counts: dict[str, int] = {}
    challenge_counts: dict[str, int] = {}
    for e in entries:
        diff = e.get("difficulty", "unknown")
        diff_counts[diff] = diff_counts.get(diff, 0) + 1
        intent = e.get("expected_intent", "unknown")
        intent_counts[intent] = intent_counts.get(intent, 0) + 1
        challenge = e.get("retrieval_challenge") or "untagged"
        challenge_counts[challenge] = challenge_counts.get(challenge, 0) + 1

    logger.info("Difficulty distribution: %s", diff_counts)
    logger.info("Intent distribution: %s", dict(sorted(intent_counts.items())))
    logger.info("Retrieval challenge distribution: %s", dict(sorted(challenge_counts.items())))


# ---------------------------------------------------------------------------
# Optional Stage 1 extension — LLM-based query generation
# ---------------------------------------------------------------------------

def stage1_llm_generate(
    notes: list[NoteRecord],
    max_notes: int = 100,
    seed: int = 42,
) -> list[CandidateEntry]:
    """
    Use Gemini to generate 2 queries per note (one keyword, one question).

    Generates for a random sample of max_notes notes to limit LLM API calls.
    Only called when --llm-queries is passed.
    """
    import random
    rng = random.Random(seed)
    sampled = rng.sample(notes, min(max_notes, len(notes)))

    try:
        from app.services.llm_service import LLMService
    except Exception as exc:
        logger.error("LLM service unavailable: %s", exc)
        return []

    entries: list[CandidateEntry] = []
    for note in sampled:
        preview = (note.content or "")[:400].strip()
        if not preview:
            continue

        prompt = (
            f"You are generating search queries for a personal knowledge base.\n\n"
            f"Note title: {note.title}\n"
            f"Note content (preview): {preview}\n\n"
            f"Generate exactly 2 queries a user might use to find this note:\n"
            f"1. A keyword-style phrase (2-5 words, noun phrase only, no verbs)\n"
            f"2. A natural language question (starts with How/What/When/Show/Find)\n\n"
            f"Respond with ONLY these two lines, no explanations:\n"
            f"KEYWORD: <keyword phrase>\n"
            f"QUESTION: <natural question>"
        )

        try:
            response = LLMService.generate(prompt=prompt)
            kw_line = next((l for l in response.splitlines() if l.startswith("KEYWORD:")), None)
            nl_line = next((l for l in response.splitlines() if l.startswith("QUESTION:")), None)

            if kw_line:
                kw = kw_line.replace("KEYWORD:", "").strip()
                if 2 <= len(kw.split()) <= 8:
                    entries.append(CandidateEntry(
                        primary_note_id=note.id,
                        query=kw,
                        query_type="llm_kw",
                        relevant_note_ids=[note.id],
                        expected_intent="general",
                        expected_category="General",
                        difficulty="medium",
                        tags=["llm_generated"],
                        retrieval_challenge="lexical",
                    ))

            if nl_line:
                nl = nl_line.replace("QUESTION:", "").strip()
                if len(nl.split()) >= 3:
                    entries.append(CandidateEntry(
                        primary_note_id=note.id,
                        query=nl,
                        query_type="llm_nl",
                        relevant_note_ids=[note.id],
                        expected_intent="question",
                        expected_category="Questions",
                        difficulty="medium",
                        tags=["llm_generated"],
                        retrieval_challenge="semantic",
                    ))

        except Exception as exc:
            logger.debug("LLM generation failed for note %d: %s", note.id, exc)
            continue

    logger.info("LLM generation: produced %d candidates from %d notes", len(entries), len(sampled))
    return entries


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate retrieval benchmark candidates.")
    p.add_argument("--user-id", type=int, default=1)
    p.add_argument("--output-dir", type=str, default="app/evaluation/benchmark")
    p.add_argument("--expand-relevance", action="store_true",
                   help="Stage 2: expand relevant set via retrieve_hybrid().")
    p.add_argument("--dedup", action="store_true",
                   help="Stage 3: remove near-duplicate queries via embedding similarity.")
    p.add_argument("--llm-queries", action="store_true",
                   help="Stage 1 extension: generate additional queries via Gemini LLM.")
    p.add_argument("--llm-max-notes", type=int, default=50,
                   help="Max notes to generate LLM queries for (default 50).")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    db = SessionLocal()
    try:
        notes = load_notes(db, args.user_id)
        logger.info("Loaded %d organized notes for user_id=%d", len(notes), args.user_id)

        if len(notes) < 10:
            logger.warning("Very few notes loaded — results will be sparse.")

        # Stage 1: Template candidates
        candidates = stage1_template_candidates(notes)
        logger.info("Stage 1 (templates): %d candidates", len(candidates))

        # Stage 1 extension: LLM queries
        if args.llm_queries:
            llm_candidates = stage1_llm_generate(notes, max_notes=args.llm_max_notes)
            candidates.extend(llm_candidates)
            logger.info("Stage 1 (LLM): total %d candidates", len(candidates))

        # Stage 2: Retrieval expansion
        if args.expand_relevance:
            candidates = stage2_expand_relevance(candidates, args.user_id, db)
            logger.info("Stage 2 (expand): done")
        else:
            logger.info("Stage 2 (expand): skipped (pass --expand-relevance to enable)")

    finally:
        db.close()

    # Stage 3: Deduplication (runs outside DB session — uses embedding model)
    if args.dedup:
        candidates = stage3_dedup(candidates)
    else:
        logger.info("Stage 3 (dedup): skipped (pass --dedup to enable)")

    # Stage 4: Quality filter
    candidates = stage4_quality_filter(candidates)

    # Stage 5: Export
    stage5_export(candidates, out, note_count=len(notes) if 'notes' in dir() else 0)
    logger.info("Done. Candidates written to %s", out / "candidates.json")
    logger.info("Run human_eval.py to review and move to verified.json.")


if __name__ == "__main__":
    main()
