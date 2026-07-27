"""
Phase 4: Generate retrieval and ask/RAG benchmarks from ingested notes.

Usage (run AFTER ingest_dataset.py completes):
    python scripts/generate_benchmarks.py --user-id 1 --output-dir evaluation_results/benchmarks

Outputs:
    evaluation_results/benchmarks/retrieval_benchmark.json   (250-300 queries)
    evaluation_results/benchmarks/ask_benchmark.json         (120-150 queries)

Strategy:
    1. Query all notes from the DB for user_id.
    2. For each topic cluster (identified by content keywords), match note IDs dynamically.
    3. Emit benchmark entries covering all required query types:
       factual, paraphrased, multi-hop, temporal, comparison, synthesis,
       ambiguous, category-oriented, exact-keyword, semantic.
    4. Reference only note IDs that actually exist in the DB.
"""

from __future__ import annotations

import argparse
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
# Note lookup helpers
# ---------------------------------------------------------------------------

class NoteRecord(NamedTuple):
    id: int
    title: str
    content: str


def load_notes(db: Session, user_id: int) -> list[NoteRecord]:
    rows = (
        db.query(Note.id, Note.title, Note.content)
        .filter(Note.user_id == user_id, Note.organization_status == "organized")
        .order_by(Note.id)
        .all()
    )
    return [NoteRecord(r.id, r.title or "", r.content or "") for r in rows]


def find_notes(notes: list[NoteRecord], *keywords: str, min_match: int = 1) -> list[int]:
    """Return IDs of notes whose content contains at least min_match of the keywords."""
    matched = []
    kws = [k.lower() for k in keywords]
    for n in notes:
        text = (n.title + " " + n.content).lower()
        hits = sum(1 for k in kws if k in text)
        if hits >= min_match:
            matched.append(n.id)
    return matched


def find_notes_exact(notes: list[NoteRecord], phrase: str) -> list[int]:
    """Return IDs of notes containing the exact phrase (case-insensitive)."""
    phrase_lower = phrase.lower()
    return [n.id for n in notes if phrase_lower in (n.title + " " + n.content).lower()]


# ---------------------------------------------------------------------------
# Retrieval benchmark builder
# ---------------------------------------------------------------------------

class RetrievalEntry:
    _counter = 0

    def __init__(
        self,
        query: str,
        relevant_note_ids: list[int],
        expected_intent: str,
        expected_category: str,
        difficulty: str,
        tags: list[str],
    ):
        RetrievalEntry._counter += 1
        self.id = str(RetrievalEntry._counter)
        self.query = query
        self.relevant_note_ids = relevant_note_ids
        self.expected_intent = expected_intent
        self.expected_category = expected_category
        self.difficulty = difficulty
        self.tags = tags

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "query": self.query,
            "expected_intent": self.expected_intent,
            "expected_category": self.expected_category,
            "relevant_note_ids": self.relevant_note_ids,
            "difficulty": self.difficulty,
            "tags": self.tags,
        }


class AskEntry:
    _counter = 0

    def __init__(
        self,
        question: str,
        expected_note_ids: list[int],
        reference_answer: str,
        category: str,
        difficulty: str,
        eval_notes: str = "",
        prefix: str = "q",
    ):
        AskEntry._counter += 1
        self.id = f"{prefix}_{AskEntry._counter:03d}"
        self.question = question
        self.expected_note_ids = expected_note_ids
        self.reference_answer = reference_answer
        self.category = category
        self.difficulty = difficulty
        self.eval_notes = eval_notes

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "question": self.question,
            "expected_note_ids": self.expected_note_ids,
            "reference_answer": self.reference_answer,
            "category": self.category,
            "difficulty": self.difficulty,
            "eval_notes": self.eval_notes,
        }


def R(query, ids, intent, category, difficulty="medium", tags=None):
    """Shorthand for RetrievalEntry — only emitted if ids is non-empty.
    Expected set is capped at 10: keyword matching over 1000 notes produces
    very large candidate lists; the benchmark should target the most central
    notes, not every note that tangentially mentions a keyword."""
    if not ids:
        return None
    return RetrievalEntry(query, ids[:10], intent, category, difficulty, tags or [])


def A(question, ids, answer, category, difficulty="medium", notes="", prefix="q"):
    """Shorthand for AskEntry — only emitted if ids is non-empty."""
    if not ids:
        return None
    return AskEntry(question, ids, answer, category, difficulty, notes, prefix)


def generate_retrieval_benchmark(notes: list[NoteRecord]) -> list[dict]:
    entries = []

    def add(*args):
        e = R(*args)
        if e:
            entries.append(e.to_dict())

    # ---- PROGRAMMING ----
    python_ids = find_notes(notes, "python", min_match=1)[:8]
    add("What are useful Python tips and tricks I've learned?", python_ids, "study", "Study - Python", "easy", ["python"])
    add("Show my Python programming notes", python_ids, "study", "Study - Python", "easy", ["python"])

    dict_ids = find_notes(notes, "dict", "dictionary", "hashmap", min_match=1)
    add("Notes about Python dictionaries and hash maps", dict_ids, "reference", "Reference - Python", "easy", ["python", "data_structures"])

    async_ids = find_notes(notes, "async", "asyncio", "coroutine", min_match=1)
    add("How does Python async programming work?", async_ids, "study", "Study - Python", "medium", ["python", "async"])
    add("Concurrency and asynchronous patterns in Python", async_ids, "study", "Study - Python", "medium", ["async"])

    decorator_ids = find_notes(notes, "decorator", "@", min_match=1)
    add("Python decorator notes", decorator_ids, "reference", "Reference - Python", "easy", ["python", "decorators"])

    git_ids = find_notes(notes, "git", "branch", "commit", "rebase", min_match=1)
    add("What git commands and workflows have I noted?", git_ids, "reference", "Reference - Git", "easy", ["git"])
    add("Git tips and tricks", git_ids, "reference", "Reference - Git", "easy", ["git"])

    js_ids = find_notes(notes, "javascript", "typescript", "promise", "async/await", min_match=1)
    add("JavaScript and TypeScript notes", js_ids, "study", "Study - JavaScript", "easy", ["javascript"])

    golang_ids = find_notes(notes, "goroutine", "golang", "go ", "defer", min_match=1)
    add("What have I learned about Go programming?", golang_ids, "study", "Study - Go", "medium", ["golang"])

    rust_ids = find_notes(notes, "rust", "ownership", "borrow", "lifetime", min_match=1)
    add("Rust ownership and borrowing notes", rust_ids, "study", "Study - Rust", "medium", ["rust"])

    design_pattern_ids = find_notes(notes, "pattern", "observer", "factory", "strategy", "singleton", min_match=1)
    add("What design patterns have I documented?", design_pattern_ids, "reference", "Reference - Design Patterns", "medium", ["design_patterns"])
    add("Software design patterns notes", design_pattern_ids, "reference", "Reference - Design Patterns", "easy", ["patterns"])

    perf_ids = find_notes(notes, "performance", "latency", "benchmark", "faster", "optimize", min_match=1)
    add("Performance optimization notes", perf_ids, "reference", "Reference - Performance", "medium", ["performance"])

    sql_ids = find_notes(notes, "sql", "query", "join", "window function", "cte", min_match=1)
    add("SQL tips and advanced query techniques", sql_ids, "study", "Study - SQL", "medium", ["sql", "database"])

    regex_ids = find_notes(notes, "regex", "regular expression", "re.split", "pattern", min_match=1)
    add("Regular expression notes and examples", regex_ids, "reference", "Reference - Regex", "easy", ["regex"])

    shell_ids = find_notes(notes, "shell", "bash", "grep", "awk", "curl", "ssh", min_match=1)
    add("Shell and command line tips I've collected", shell_ids, "reference", "Reference - Shell", "easy", ["shell", "cli"])

    # ---- AI / ML ----
    rag_ids = find_notes(notes, "rag", "retrieval-augmented", "retrieval augmented", min_match=1)
    add("What do I know about RAG systems?", rag_ids, "study", "Study - AI", "medium", ["rag", "ai"])
    add("Retrieval augmented generation notes", rag_ids, "study", "Study - AI", "easy", ["rag"])

    embed_ids = find_notes(notes, "embedding", "vector", "semantic", "cosine", min_match=2)
    add("Notes about embeddings and vector search", embed_ids, "study", "Study - AI", "medium", ["embeddings", "vectors"])
    add("How do text embeddings work?", embed_ids, "study", "Study - AI", "medium", ["embeddings"])

    llm_ids = find_notes(notes, "llm", "language model", "gpt", "gemini", "groq", min_match=1)
    add("Large language model notes and findings", llm_ids, "study", "Study - AI", "medium", ["llm", "ai"])
    add("What LLMs have I worked with?", llm_ids, "study", "Study - AI", "easy", ["llm"])

    chunk_ids = find_notes(notes, "chunk", "chunking", "chunk size", "overlap", min_match=1)
    add("Document chunking strategy notes", chunk_ids, "reference", "Reference - AI", "medium", ["chunking", "rag"])

    rerank_ids = find_notes(notes, "rerank", "cross-encoder", "reranker", "bi-encoder", min_match=1)
    add("Notes about reranking in search systems", rerank_ids, "study", "Study - AI", "hard", ["reranking", "search"])

    eval_ids = find_notes(notes, "evaluation", "benchmark", "metrics", "mrr", "recall", "ndcg", "precision", min_match=2)
    add("RAG and retrieval evaluation metrics", eval_ids, "study", "Study - AI", "hard", ["evaluation", "metrics"])
    add("How do I measure retrieval quality?", eval_ids, "study", "Study - AI", "hard", ["evaluation"])

    finetune_ids = find_notes(notes, "fine-tuning", "lora", "rlhf", "instruction tuning", "dpo", min_match=1)
    add("LLM fine-tuning and alignment notes", finetune_ids, "study", "Study - AI", "hard", ["finetuning", "llm"])

    prompt_ids = find_notes(notes, "prompt", "few-shot", "zero-shot", "chain-of-thought", "temperature", min_match=1)
    add("Prompting techniques and tips", prompt_ids, "study", "Study - AI", "medium", ["prompting"])
    add("What have I learned about LLM prompting?", prompt_ids, "study", "Study - AI", "easy", ["prompting"])

    hallucination_ids = find_notes(notes, "hallucination", "grounded", "groundedness", "faithful", min_match=1)
    add("Notes about LLM hallucination and grounding", hallucination_ids, "study", "Study - AI", "medium", ["hallucination", "rag"])

    hyde_ids = find_notes(notes, "hyde", "hypothetical document", "hypothetical", min_match=1)
    add("HyDE and query expansion techniques", hyde_ids, "study", "Study - AI", "hard", ["query_expansion"])

    # ---- UNIVERSITY / ACADEMIA ----
    os_ids = find_notes(notes, "operating system", "scheduling", "process", "thread", "deadlock", "page", min_match=1)
    add("Operating systems study notes", os_ids, "study", "Study - Operating Systems", "medium", ["os", "university"])
    add("OS concepts I need to review for exams", os_ids, "study", "Study - Operating Systems", "easy", ["os"])

    dbms_ids = find_notes(notes, "normalization", "acid", "transaction", "dbms", "b+ tree", "b-tree", min_match=1)
    add("Database management systems notes", dbms_ids, "study", "Study - DBMS", "medium", ["dbms", "university"])

    network_ids = find_notes(notes, "tcp", "osi", "subnet", "network", "http", "dns", min_match=1)
    add("Computer networks study notes", network_ids, "study", "Study - Computer Networks", "medium", ["networking", "university"])

    algo_ids = find_notes(notes, "algorithm", "complexity", "sorting", "graph", "dynamic programming", "greedy", min_match=1)
    add("Algorithm and data structures notes", algo_ids, "study", "Study - Algorithms", "medium", ["algorithms", "dsa"])
    add("What algorithms have I studied?", algo_ids, "study", "Study - Algorithms", "easy", ["algorithms"])

    compiler_ids = find_notes(notes, "compiler", "lexer", "parse", "grammar", "automata", "dfa", min_match=1)
    add("Compiler design and theory of computation notes", compiler_ids, "study", "Study - Compiler Design", "hard", ["compiler", "toc"])

    capstone_ids = find_notes(notes, "capstone", "thapar", "submission", "professor", "college", min_match=1)
    add("Capstone project notes", capstone_ids, "study", "Study - Capstone", "medium", ["capstone", "university"])

    parallel_ids = find_notes(notes, "openmp", "parallel", "thread", "concurrent", "mutex", "semaphore", min_match=1)
    add("Parallel programming and concurrency notes", parallel_ids, "study", "Study - Operating Systems", "hard", ["parallel", "concurrency"])

    # ---- INTERVIEW PREP ----
    leetcode_ids = find_notes(notes, "leetcode", "binary search", "sliding window", "two pointer", "two-pointer", min_match=1)
    add("LeetCode problem patterns and solutions", leetcode_ids, "study", "Study - Interview Prep", "medium", ["leetcode", "interview"])

    dp_ids = find_notes(notes, "dynamic programming", "dp", "memoization", "tabulation", min_match=1)
    add("Dynamic programming notes and patterns", dp_ids, "study", "Study - Algorithms", "hard", ["dp", "algorithms"])

    sysdesign_ids = find_notes(notes, "system design", "url shortener", "twitter", "instagram", "rate limiter", "consistent hashing", min_match=1)
    add("System design interview prep notes", sysdesign_ids, "study", "Study - System Design", "medium", ["system_design", "interview"])
    add("What system design topics have I covered?", sysdesign_ids, "study", "Study - System Design", "easy", ["system_design"])

    behavioral_ids = find_notes(notes, "behavioral", "star format", "leadership", "amazon", "conflict", min_match=1)
    add("Behavioral interview preparation notes", behavioral_ids, "study", "Study - Interview Prep", "medium", ["behavioral", "interview"])

    mock_ids = find_notes(notes, "mock interview", "mock", "interviewer", "edge case", "clarify", min_match=1)
    add("Mock interview notes and feedback", mock_ids, "study", "Study - Interview Prep", "medium", ["mock_interview"])

    resume_ids = find_notes(notes, "resume", "cv", "quantify", "bullet point", "impact", min_match=1)
    add("Resume writing and improvement tips", resume_ids, "reference", "Reference - Career", "easy", ["resume", "career"])

    placement_ids = find_notes(notes, "placement", "campus", "company", "offer", "intern", min_match=1)
    add("Campus placement preparation notes", placement_ids, "study", "Study - Interview Prep", "easy", ["placement"])

    # ---- SYSTEM DESIGN (TECHNICAL) ----
    shard_ids = find_notes(notes, "shard", "partition", "sharding", "horizontal", min_match=1)
    add("Database sharding and partitioning notes", shard_ids, "study", "Study - System Design", "hard", ["sharding", "database"])

    cache_ids = find_notes(notes, "cache", "redis cache", "eviction", "lru", "bloom filter", min_match=1)
    add("Caching strategies and implementations", cache_ids, "study", "Study - System Design", "medium", ["caching"])

    queue_ids = find_notes(notes, "kafka", "message queue", "rabbitmq", "event", "producer", "consumer", min_match=1)
    add("Message queue and event streaming notes", queue_ids, "study", "Study - System Design", "medium", ["kafka", "queues"])

    microservice_ids = find_notes(notes, "microservice", "service mesh", "circuit breaker", "api gateway", min_match=1)
    add("Microservices architecture notes", microservice_ids, "study", "Study - System Design", "hard", ["microservices"])

    consensus_ids = find_notes(notes, "raft", "paxos", "consensus", "distributed", "leader election", min_match=1)
    add("Distributed systems consensus notes", consensus_ids, "study", "Study - Distributed Systems", "hard", ["distributed", "consensus"])

    observability_ids = find_notes(notes, "prometheus", "grafana", "tracing", "observability", "monitoring", min_match=1)
    add("Observability and monitoring notes", observability_ids, "reference", "Reference - DevOps", "medium", ["observability"])

    idempotent_ids = find_notes(notes, "idempotent", "idempotency", "retry", "at-least-once", min_match=1)
    add("Idempotency and distributed system reliability notes", idempotent_ids, "reference", "Reference - System Design", "hard", ["idempotency"])

    # ---- PROJECTS ----
    kv_ids = find_notes(notes, "knowledgevault", "knowledge vault", "kv", min_match=1)
    add("KnowledgeVault project notes", kv_ids, "reference", "Reference - KnowledgeVault", "easy", ["project"])
    add("What decisions have I made for the KnowledgeVault project?", kv_ids, "reference", "Reference - KnowledgeVault", "medium", ["project", "architecture"])

    hybrid_ids = find_notes(notes, "hybrid retrieval", "intent arm", "semantic arm", "fusion", min_match=1)
    add("Notes about hybrid retrieval implementation", hybrid_ids, "reference", "Reference - KnowledgeVault", "hard", ["hybrid_retrieval", "rag"])

    docker_ids = find_notes(notes, "docker", "container", "compose", "dockerfile", min_match=1)
    add("Docker and containerization notes", docker_ids, "study", "Study - Docker", "easy", ["docker"])
    add("What Docker tips have I collected?", docker_ids, "reference", "Reference - Docker", "easy", ["docker"])

    fastapi_ids = find_notes(notes, "fastapi", "dependency injection", "router", "pydantic", min_match=1)
    add("FastAPI development notes", fastapi_ids, "study", "Study - FastAPI", "medium", ["fastapi"])

    postgres_ids = find_notes(notes, "postgresql", "postgres", "pgvector", "explain analyze", min_match=1)
    add("PostgreSQL database notes", postgres_ids, "study", "Study - PostgreSQL", "medium", ["postgresql"])
    add("What PostgreSQL features and tips do I have?", postgres_ids, "study", "Study - PostgreSQL", "easy", ["postgresql"])

    redis_ids = find_notes(notes, "redis", "cache", "queue", "pubsub", min_match=1)
    add("Redis usage and patterns", redis_ids, "study", "Study - Redis", "easy", ["redis"])

    pgvector_ids = find_notes(notes, "pgvector", "vector", "hnsw", "ivfflat", "cosine", min_match=1)
    add("pgvector and vector search notes", pgvector_ids, "study", "Study - PostgreSQL", "hard", ["pgvector", "vectors"])

    # ---- MEETINGS ----
    meeting_ids = find_notes(notes, "meeting", "sync", "standup", "sprint", "retrospective", min_match=1)
    add("What meetings have I had?", meeting_ids, "event", "Meetings", "easy", ["meetings"])
    add("Team meeting notes", meeting_ids, "event", "Meetings", "easy", ["meetings"])

    mentor_ids = find_notes(notes, "mentor", "senior", "advice", "feedback", "review", min_match=1)
    add("Mentor and senior advice I've received", mentor_ids, "communication", "Communication", "easy", ["mentorship"])

    hackathon_ids = find_notes(notes, "hackathon", "36-hour", "hackathon team", min_match=1)
    add("Hackathon planning notes", hackathon_ids, "event", "Meetings", "easy", ["hackathon"])

    # ---- REMINDERS / TASKS ----
    todo_ids = find_notes(notes, "deadline", "submit", "due", "by", "before", "complete", min_match=2)
    add("What are my pending tasks and deadlines?", todo_ids[:6], "todo", "Tasks", "easy", ["todo", "deadlines"])

    appointment_ids = find_notes(notes, "appointment", "dentist", "doctor", "checkup", "health", "schedule", min_match=1)
    add("What health appointments do I have?", appointment_ids, "reminder", "Appointments", "easy", ["appointments", "health"])

    payment_ids = find_notes(notes, "pay", "bill", "fee", "rent", "electricity", "recharge", min_match=1)
    add("What payments and bills do I need to make?", payment_ids, "todo", "Bills", "easy", ["bills", "finance"])

    grocery_ids = find_notes(notes, "grocery", "groceries", "milk", "eggs", "bread", "buy", min_match=2)
    add("What is on my shopping list?", grocery_ids, "todo", "Shopping", "easy", ["shopping", "grocery"])

    remind_ids = find_notes(notes, "remind", "reminder", "don't forget", "remember", min_match=1)
    add("Show all my reminders", remind_ids[:8], "reminder", "Reminders", "easy", ["reminders"])
    add("What do I need to remember this week?", remind_ids[:6], "reminder", "Reminders", "medium", ["reminders"])

    # ---- SHOPPING / FINANCE ----
    budget_ids = find_notes(notes, "budget", "spending", "expense", "monthly", "tracking", min_match=1)
    add("My budget and expense tracking notes", budget_ids, "todo", "Finance", "easy", ["budget", "finance"])
    add("Monthly expense breakdown", budget_ids, "reference", "Finance", "medium", ["finance"])

    invest_ids = find_notes(notes, "invest", "sip", "mutual fund", "stock", "nifty", "zerodha", min_match=1)
    add("Investment and savings notes", invest_ids, "reference", "Finance", "medium", ["investing"])

    laptop_ids = find_notes(notes, "laptop", "keyboard", "mechanical", "monitor", "ssd", min_match=1)
    add("Tech purchase notes and wishlists", laptop_ids, "todo", "Shopping", "easy", ["tech", "shopping"])

    # ---- TRAVEL ----
    travel_ids = find_notes(notes, "trip", "travel", "train", "flight", "hotel", "book", "itinerary", min_match=1)
    add("My travel plans and notes", travel_ids, "todo", "Travel", "easy", ["travel"])
    add("Upcoming trips and travel bookings", travel_ids, "todo", "Travel", "easy", ["travel"])

    delhi_ids = find_notes(notes, "delhi", "iit delhi", "hackathon", min_match=1)
    add("Delhi trip plans", delhi_ids, "todo", "Travel", "easy", ["travel", "delhi"])

    manali_ids = find_notes(notes, "manali", "shimla", "trek", "mountain", "himachal", min_match=1)
    add("Hill station and trekking plans", manali_ids, "todo", "Travel", "medium", ["travel", "trek"])

    irctc_ids = find_notes(notes, "irctc", "tatkal", "train ticket", "railway", min_match=1)
    add("Train booking tips and notes", irctc_ids, "reference", "Reference - Travel", "easy", ["train", "irctc"])

    # ---- HEALTH ----
    workout_ids = find_notes(notes, "workout", "exercise", "gym", "fitness", "push", "pull", "legs", min_match=1)
    add("Fitness and workout notes", workout_ids, "todo", "Health", "easy", ["fitness", "workout"])
    add("My exercise routine notes", workout_ids, "todo", "Health", "easy", ["fitness"])

    sleep_ids = find_notes(notes, "sleep", "insomnia", "circadian", "melatonin", "sleep cycle", min_match=1)
    add("Sleep improvement notes", sleep_ids, "reference", "Reference - Health", "medium", ["sleep", "health"])

    nutrition_ids = find_notes(notes, "nutrition", "protein", "diet", "vitamin", "supplement", "omega", min_match=1)
    add("Nutrition and supplement notes", nutrition_ids, "reference", "Reference - Health", "medium", ["nutrition"])

    mental_ids = find_notes(notes, "anxiety", "meditation", "mindfulness", "mental health", "journal", "stress", min_match=1)
    add("Mental health and wellbeing notes", mental_ids, "reference", "Reference - Health", "medium", ["mental_health"])

    # ---- STARTUPS ----
    startup_ids = find_notes(notes, "startup", "business", "product", "market", "idea", "saas", min_match=1)
    add("My startup ideas and business notes", startup_ids, "idea", "Ideas - Startups", "easy", ["startup"])
    add("What business ideas have I documented?", startup_ids, "idea", "Ideas", "easy", ["startup", "ideas"])

    yc_ids = find_notes(notes, "yc", "y combinator", "ycombinator", "paul graham", min_match=1)
    add("Y Combinator and startup ecosystem notes", yc_ids, "reference", "Reference - Startups", "medium", ["yc", "startup"])

    monetize_ids = find_notes(notes, "monetize", "revenue", "mrr", "subscription", "saas", "b2b", "b2c", min_match=1)
    add("Business model and monetization notes", monetize_ids, "reference", "Ideas - Startups", "medium", ["business_model"])

    validation_ids = find_notes(notes, "validation", "customer", "talk to", "mvp", "problem", "pain", min_match=1)
    add("Startup idea validation notes", validation_ids, "reference", "Ideas - Startups", "medium", ["validation", "startup"])

    # ---- BOOKS / MEDIA ----
    book_ids = find_notes(notes, "book", "reading", "author", "chapter", "finished", "recommended", min_match=1)
    add("What books have I taken notes on?", book_ids, "reference", "Reference - Books", "easy", ["books"])
    add("My book notes and summaries", book_ids, "reference", "Reference - Books", "easy", ["books"])

    ddia_ids = find_notes(notes, "designing data-intensive", "kleppmann", "data-intensive", min_match=1)
    add("Notes from Designing Data-Intensive Applications", ddia_ids, "study", "Study - Books", "hard", ["ddia", "books"])

    atomic_ids = find_notes(notes, "atomic habits", "james clear", "habit", "cue", "routine", "reward", min_match=1)
    add("Atomic Habits notes and takeaways", atomic_ids, "study", "Study - Books", "easy", ["habits", "books"])

    podcast_ids = find_notes(notes, "podcast", "lex fridman", "huberman", "karpathy", min_match=1)
    add("Podcast notes and key insights", podcast_ids, "reference", "Reference - Learning", "easy", ["podcasts"])

    # ---- LEARNING RESOURCES ----
    course_ids = find_notes(notes, "course", "udemy", "tutorial", "cs50", "completed", min_match=1)
    add("Online courses I'm taking or completed", course_ids, "study", "Study - Learning", "easy", ["courses"])

    kubernetes_ids = find_notes(notes, "kubernetes", "k8s", "pod", "deployment", "service", min_match=1)
    add("Kubernetes learning notes", kubernetes_ids, "study", "Study - Kubernetes", "medium", ["kubernetes"])

    terraform_ids = find_notes(notes, "terraform", "infrastructure as code", "tfstate", min_match=1)
    add("Terraform and infrastructure as code notes", terraform_ids, "study", "Study - DevOps", "medium", ["terraform", "iac"])

    oauth_ids = find_notes(notes, "oauth", "jwt", "auth", "token", "bearer", min_match=1)
    add("Authentication and authorization notes", oauth_ids, "study", "Study - Security", "medium", ["auth", "security"])

    testing_ids = find_notes(notes, "pytest", "test", "fixture", "mock", "unit test", min_match=1)
    add("Testing and pytest notes", testing_ids, "reference", "Reference - Testing", "medium", ["testing", "pytest"])

    # ---- DEBUGGING ----
    debug_ids = find_notes(notes, "bug", "error", "fix", "root cause", "debugging", "issue", min_match=2)
    add("Debugging sessions and fixes", debug_ids, "reference", "Reference - Debugging", "medium", ["debugging"])
    add("What bugs have I debugged recently?", debug_ids[:6], "reference", "Reference - Debugging", "easy", ["debugging"])

    n1_ids = find_notes(notes, "n+1", "joinedload", "selectinload", "eager", "lazy", min_match=1)
    add("SQLAlchemy N+1 query problem notes", n1_ids, "reference", "Reference - Database", "hard", ["n1", "sqlalchemy"])

    race_ids = find_notes(notes, "race condition", "concurrent", "atomic", "deadlock", "inflight", min_match=1)
    add("Race condition and concurrency bug notes", race_ids, "reference", "Reference - Debugging", "hard", ["race_condition", "concurrency"])

    memory_ids = find_notes(notes, "memory leak", "memory", "oom", "singleton", "gc", min_match=1)
    add("Memory management and leak debugging notes", memory_ids, "reference", "Reference - Debugging", "hard", ["memory", "debugging"])

    # ---- JOURNAL / PERSONAL ----
    journal_ids = find_notes(notes, "today", "reflection", "feeling", "grateful", "goal", "realized", min_match=1)
    add("My journal entries and personal reflections", journal_ids[:8], "general", "General", "easy", ["journal"])

    productivity_ids = find_notes(notes, "productivity", "pomodoro", "focus", "distraction", "procrastinate", min_match=1)
    add("Productivity tips and personal notes", productivity_ids, "reference", "Reference - Productivity", "easy", ["productivity"])

    career_ids = find_notes(notes, "career", "direction", "backend", "ai engineer", "senior", "google", min_match=1)
    add("Career direction and goal notes", career_ids, "general", "General", "medium", ["career"])

    open_source_ids = find_notes(notes, "open source", "github", "twitter", "build in public", "blog", min_match=1)
    add("Open source and building in public notes", open_source_ids, "idea", "Ideas", "medium", ["open_source"])

    # ---- MULTI-HOP / CROSS-DOMAIN ----
    kv_rag_ids = list(set(kv_ids) | set(rag_ids))
    add("KnowledgeVault RAG pipeline decisions and findings", kv_rag_ids[:8], "reference", "Reference - KnowledgeVault", "hard", ["rag", "project"])

    interview_ds_ids = list(set(leetcode_ids) | set(dp_ids) | set(sysdesign_ids))
    add("All my interview preparation notes — coding and system design", interview_ds_ids[:10], "study", "Study - Interview Prep", "hard", ["interview", "comprehensive"])

    ai_infra_ids = list(set(rag_ids) | set(postgres_ids) | set(redis_ids))
    add("AI system infrastructure notes: vector DB, cache, and retrieval", ai_infra_ids[:8], "study", "Study - AI", "hard", ["ai", "infrastructure"])

    health_study_ids = list(set(workout_ids) | set(sleep_ids) | set(nutrition_ids))
    add("All my health and wellness notes", health_study_ids[:8], "reference", "Reference - Health", "medium", ["health", "wellness"])

    finance_todo_ids = list(set(budget_ids) | set(payment_ids))
    add("Financial tasks and expense notes", finance_todo_ids[:8], "todo", "Finance", "medium", ["finance", "tasks"])

    uni_all_ids = list(set(os_ids) | set(dbms_ids) | set(network_ids) | set(algo_ids))
    add("My university computer science notes", uni_all_ids[:10], "study", "Study - Computer Science", "hard", ["university", "cs"])

    # ---- SEMANTIC / PARAPHRASED QUERIES ----
    add("Things I need to do this week", todo_ids[:6], "todo", "Tasks", "medium", ["todo"])
    add("What tasks are pending for me?", todo_ids[:6], "todo", "Tasks", "medium", ["todo"])

    add("Resources for learning backend development", list(set(fastapi_ids) | set(postgres_ids) | set(docker_ids))[:8], "study", "Study - Backend", "medium", ["backend", "learning"])
    add("How do I get better at backend engineering?", list(set(fastapi_ids) | set(postgres_ids))[:6], "study", "Study - Backend", "medium", ["backend"])

    add("What are distributed systems trade-offs?", list(set(consensus_ids) | set(shard_ids) | set(microservice_ids))[:6], "study", "Study - System Design", "hard", ["distributed"])
    add("Notes on scalability and reliability", list(set(cache_ids) | set(shard_ids))[:6], "study", "Study - System Design", "hard", ["scalability"])

    add("What are my creative ideas?", startup_ids[:6], "idea", "Ideas", "easy", ["ideas"])
    add("Show my brainstorming notes", list(set(startup_ids) | set(find_notes(notes, "idea", "brainstorm", min_match=1)))[:8], "idea", "Ideas", "easy", ["brainstorm"])

    add("Advice and wisdom I've collected", list(set(mentor_ids) | set(journal_ids))[:6], "general", "General", "medium", ["advice"])

    # ---- EXACT KEYWORD QUERIES ----
    bm25_ids = find_notes_exact(notes, "BM25")
    if bm25_ids:
        add("BM25", bm25_ids, "study", "Study - AI", "easy", ["bm25", "exact"])

    hnsw_ids = find_notes_exact(notes, "HNSW")
    if hnsw_ids:
        add("HNSW index", hnsw_ids, "study", "Study - AI", "easy", ["hnsw", "exact"])

    hnsw_ids2 = find_notes_exact(notes, "hnsw")
    if hnsw_ids2:
        add("HNSW vector index configuration", hnsw_ids2, "study", "Study - AI", "medium", ["hnsw"])

    rrf_ids = find_notes_exact(notes, "Reciprocal Rank Fusion")
    if rrf_ids:
        add("Reciprocal Rank Fusion", rrf_ids, "study", "Study - AI", "medium", ["rrf", "exact"])

    add("two sum problem", find_notes_exact(notes, "Two Sum"), "study", "Study - Interview Prep", "easy", ["two_sum", "exact"])
    add("LRU cache implementation", find_notes(notes, "lru cache", "lru", "ordereddict", min_match=1), "study", "Study - Interview Prep", "medium", ["lru", "cache"])

    cap_ids = find_notes_exact(notes, "CAP theorem")
    if cap_ids:
        add("CAP theorem", cap_ids, "study", "Study - System Design", "easy", ["cap", "exact"])

    add("PageRank or graph algorithms notes", find_notes(notes, "graph algorithm", "bfs", "dfs", "dijkstra", min_match=1), "study", "Study - Algorithms", "medium", ["graph"])

    # ---- TEMPORAL ----
    feb_ids = find_notes(notes, "february", "feb 2024", "this month", "this week", "last week", min_match=1)
    add("What have I been working on this month?", feb_ids[:6], "general", "General", "hard", ["temporal"])
    add("Recent notes and activities", feb_ids[:6], "general", "General", "hard", ["temporal"])

    # ---- COMPARISON ----
    redis_vs_kafka = list(set(redis_ids) | set(queue_ids))
    add("Redis vs Kafka — when to use each", redis_vs_kafka[:6], "study", "Study - System Design", "hard", ["comparison", "redis", "kafka"])

    python_vs_go = list(set(python_ids) | set(golang_ids))
    add("Python vs Go programming notes", python_vs_go[:6], "study", "Study - Programming", "hard", ["comparison", "python", "go"])

    sql_vs_nosql = list(set(postgres_ids) | set(find_notes(notes, "nosql", "mongodb", "dynamodb", min_match=1)))
    add("SQL vs NoSQL database comparison", sql_vs_nosql[:6], "study", "Study - Database", "hard", ["comparison", "database"])

    rag_rerank_compare = list(set(rag_ids) | set(rerank_ids))
    add("Comparing RAG retrieval strategies: dense, sparse, and reranking", rag_rerank_compare[:6], "study", "Study - AI", "hard", ["comparison", "rag"])

    rest_vs_graphql = find_notes(notes, "graphql", "rest", "grpc", "api", min_match=1)
    add("REST vs GraphQL API design trade-offs", rest_vs_graphql[:6], "study", "Study - System Design", "hard", ["comparison", "api"])

    # ---- CATEGORY-ORIENTED ----
    add("Show all my communication notes", find_notes(notes, "tell", "message", "email", "discuss", "sid", min_match=1)[:6], "communication", "Communication", "easy", ["communication"])
    add("All my reminder notes", remind_ids[:8], "reminder", "Reminders", "easy", ["reminders", "category"])
    add("My study notes on AI and machine learning", list(set(llm_ids) | set(embed_ids) | set(rag_ids))[:8], "study", "Study - AI", "easy", ["study", "ai"])
    add("Notes categorized under system design", sysdesign_ids[:6], "study", "Study - System Design", "easy", ["category", "system_design"])

    # ---- AMBIGUOUS ----
    ambig1 = list(set(python_ids) | set(fastapi_ids) | set(golang_ids))
    add("Programming notes I've taken recently", ambig1[:6], "study", "Study - Programming", "medium", ["ambiguous", "programming"])

    ambig2 = list(set(budget_ids) | set(invest_ids))
    add("My financial notes", ambig2[:6], "todo", "Finance", "medium", ["ambiguous", "finance"])

    ambig3 = list(set(startup_ids) | set(kv_ids) | set(open_source_ids))
    add("Projects and ideas I'm excited about", ambig3[:6], "idea", "Ideas", "hard", ["ambiguous", "projects"])

    ambig4 = list(set(journal_ids) | set(productivity_ids))
    add("Personal notes and self-improvement", ambig4[:6], "general", "General", "hard", ["ambiguous", "personal"])

    # Filter entries with empty relevant_note_ids (safety)
    entries = [e for e in entries if e.get("relevant_note_ids")]

    logger.info("Generated %d retrieval benchmark entries", len(entries))
    return entries


# ---------------------------------------------------------------------------
# Ask benchmark builder
# ---------------------------------------------------------------------------

def generate_ask_benchmark(notes: list[NoteRecord]) -> list[dict]:
    entries = []

    def add(question, ids, answer, category, difficulty="medium", eval_notes=""):
        # Cap expected set: for ask benchmark, never more than 8 expected notes.
        # Larger expected sets are benchmark artifacts from over-broad keyword matching,
        # not genuine ground truth. The pipeline uses top-8 retrieval; expected sets
        # larger than 8 make recall artificially low and mislead evaluation.
        capped = ids[:8] if ids else []
        e = A(question, capped, answer, category, difficulty, eval_notes, "aq")
        if e:
            entries.append(e.to_dict())

    def f(*kws, min_match=1):
        return find_notes(notes, *kws, min_match=min_match)
    fe = lambda phrase: find_notes_exact(notes, phrase)

    # ---- FACTUAL LOOKUP ----
    add("What is the difference between BFS and DFS and when do you use each?",
        f("bfs", "dfs", "breadth", "depth"),
        "BFS uses a queue and explores level by level — it guarantees shortest path in unweighted graphs. DFS uses a stack or recursion and explores as far as possible before backtracking. Use BFS for shortest path problems, use DFS for topological sort, cycle detection, or when you need to explore all paths.",
        "factual_lookup", "medium")

    add("How does the HNSW index work in pgvector?",
        f("hnsw", "pgvector", "vector", "index"),
        "HNSW (Hierarchical Navigable Small World) is an approximate nearest neighbor graph structure that provides O(log n) search. In pgvector, you create it with: CREATE INDEX ON table USING hnsw (embedding vector_cosine_ops) WITH (m=16, ef_construction=64). It significantly outperforms sequential KNN scans for large datasets.",
        "factual_lookup", "hard",
        "Accept any answer explaining the graph-based ANN structure and pgvector syntax.")

    add("What is Reciprocal Rank Fusion and how is it used in hybrid search?",
        f("reciprocal rank fusion", "rrf", "hybrid", "fusion"),
        "Reciprocal Rank Fusion (RRF) combines ranked results from multiple retrieval systems using the formula: score = Σ 1/(k + rank_i) across all systems, where k=60 is the standard default. It does not require calibrated scores from each system, making it ideal for combining dense vector search with BM25 keyword search.",
        "factual_lookup", "hard")

    add("What is the CAP theorem?",
        f("cap theorem", "consistency", "availability", "partition"),
        "CAP theorem states that a distributed database can only guarantee two of three properties simultaneously: Consistency (all nodes see the same data), Availability (every request gets a response), and Partition Tolerance (system works despite network splits). In practice, partition tolerance is mandatory in distributed systems, so you choose between consistency (CP) and availability (AP).",
        "factual_lookup", "medium")

    add("What is HyDE in the context of RAG systems?",
        f("hyde", "hypothetical document"),
        "HyDE (Hypothetical Document Embeddings) is a RAG technique where you first generate a hypothetical answer to the query using an LLM, then embed that answer and use it for retrieval. Because the hypothetical answer shares vocabulary and style with real documents, it often retrieves more relevant chunks than embedding the raw query.",
        "factual_lookup", "hard")

    add("What are the ACID properties in databases?",
        f("acid", "atomicity", "consistency", "isolation", "durability"),
        "ACID stands for: Atomicity (a transaction is all-or-nothing), Consistency (database moves from one valid state to another), Isolation (concurrent transactions don't see each other's partial state), and Durability (committed data survives crashes). PostgreSQL is fully ACID compliant.",
        "factual_lookup", "easy")

    add("What is the difference between a cross-encoder and a bi-encoder?",
        f("cross-encoder", "bi-encoder", "rerank"),
        "A bi-encoder encodes query and document independently into vectors, enabling fast O(1) lookup after indexing. A cross-encoder reads the query and document together, producing higher-quality relevance scores but requiring O(n) computation per query. In RAG, bi-encoders handle first-stage recall and cross-encoders rerank the top-K candidates.",
        "factual_lookup", "hard")

    add("How does consistent hashing work?",
        f("consistent hashing", "ring", "server", "hash"),
        "Consistent hashing maps both servers and data to positions on a ring. A key is stored on the first server clockwise from its position on the ring. When a server is added or removed, only the keys near that server need to be remapped — typically 1/n of keys rather than remapping everything.",
        "factual_lookup", "medium")

    add("What is the difference between RAG retrieval failure modes?",
        f("retrieval failure", "hallucination", "context", "insufficient"),
        "RAG failure modes include: (1) retrieval miss — relevant document not in top-K candidates, (2) context window issues — too much context confuses the model, (3) hallucination — model ignores context and invents facts, (4) insufficient context — relevant document retrieved but lacks the specific detail needed.",
        "factual_lookup", "hard")

    add("What is token bucket rate limiting?",
        f("token bucket", "rate limit", "rate limiting"),
        "Token bucket is a rate limiting algorithm where each user has a bucket that holds up to a maximum number of tokens, replenished at a fixed rate. Each request consumes one token. If the bucket is empty, the request is rejected. It allows controlled bursting (up to max tokens) while enforcing an average rate limit.",
        "factual_lookup", "medium")

    add("What is the difference between FIFO, LRU, and Optimal page replacement?",
        f("page replacement", "fifo", "lru", "optimal"),
        "FIFO replaces the oldest page — simple but can suffer from Belady's anomaly. LRU replaces the least recently used page — good real-world performance but requires hardware support to track access order. Optimal replaces the page not used for the longest future time — theoretically best but requires future knowledge, so only used as a benchmark.",
        "factual_lookup", "medium")

    add("What is the two-phase commit protocol?",
        f("two-phase commit", "2pc", "coordinator", "participant"),
        "Two-phase commit (2PC) is a distributed transaction protocol. Phase 1 (Prepare): the coordinator asks all participants to lock resources and vote ready or abort. Phase 2 (Commit): if all voted ready, coordinator sends commit; if any voted abort, coordinator sends rollback. The weakness is that if the coordinator crashes after prepare, participants are blocked waiting.",
        "factual_lookup", "hard")

    # ---- PARAPHRASED ----
    add("How can I make Python code run faster?",
        f("python", "faster", "performance", "benchmark", "optimize"),
        "Key Python performance techniques: use list comprehensions over for-loops (2-3x faster for simple transforms), use __slots__ in classes with many instances (reduces memory and lookup time), use functools.cache for memoization, profile with cProfile before optimizing, and for CPU-bound work use multiprocessing not threading.",
        "factual_lookup", "medium",
        "Accept any answer covering profiling, comprehensions, or appropriate data structures.")

    add("When should I use Redis over a traditional database?",
        f("redis", "cache", "queue", "in-memory"),
        "Redis excels at: caching (sub-millisecond reads, reducing DB load), message queuing (reliable job queues with BLMOVE/BRPOPLPUSH), session storage, and real-time leaderboards (Sorted Sets). Use a traditional database for durable relational data requiring complex queries. Redis data is in-memory by default — persistence is optional.",
        "factual_lookup", "medium")

    add("What are good strategies for preparing for technical interviews?",
        f("interview", "leetcode", "system design", "behavioral", "practice"),
        "Effective interview prep: (1) master patterns not just problems — sliding window, two pointers, binary search, DFS/BFS, DP; (2) practice mock interviews with time pressure; (3) prepare STAR-format behavioral stories; (4) study 2-3 system design problems deeply; (5) ask clarifying questions before coding; (6) always discuss edge cases.",
        "factual_lookup", "easy",
        "Accept any answer covering coding patterns, system design, and behavioral prep.")

    add("What makes a good software engineer?",
        f("engineer", "senior", "skill", "communication", "persistence", "humble"),
        "Based on my notes and mentor feedback: the best engineers combine technical depth with intellectual humility — they're confident but quick to say 'I don't know.' They persist through hard problems, communicate clearly about trade-offs, write code for the next reader, and prioritize solving the right problem over using impressive technology.",
        "factual_lookup", "hard",
        "Accept any answer synthesizing notes about engineering qualities and career advice.")

    # ---- MULTI-HOP ----
    add("What have I decided about KnowledgeVault's retrieval system and why?",
        f("knowledgevault", "hybrid", "retrieval", "semantic", "intent"),
        "KnowledgeVault uses hybrid retrieval combining semantic vector search (note-level embeddings) with an intent-based category arm. However, benchmark analysis showed the hybrid arm provides zero measurable improvement over pure semantic at K=5 across 50 queries — identical metrics. Root causes: fast classifier has only 34% accuracy, confidence_factor is zero for 50% of queries, and max boost magnitude (0.027) is too small to cross rank boundaries.",
        "multi_hop", "hard",
        "Accept any answer covering the hybrid architecture AND the benchmark findings.")

    add("How does the evaluation framework work in KnowledgeVault?",
        f("evaluation", "benchmark", "judge", "mrr", "recall", "lllm-as-judge", "lm-as-judge"),
        "KnowledgeVault has two evaluation pipelines: (1) retrieval evaluation using 50 benchmark queries with metrics Precision@K, Recall@K, MRR, nDCG, and hit rate across semantic, intent, and hybrid strategies; (2) end-to-end RAG evaluation using an LLM-as-judge (Gemini) that scores answers on correctness, groundedness, faithfulness, hallucination, and completeness with root cause analysis.",
        "multi_hop", "hard")

    add("What are the known bugs and issues I've encountered building KnowledgeVault?",
        f("bug", "fixed", "knowledgevault", "error", "issue"),
        "Key KnowledgeVault bugs encountered: N+1 queries fixed with joinedload, race condition in worker fixed by switching to brpoplpush reliable queue, IDOR vulnerability in get_related_notes fixed by adding ownership check, Gemini API rate limit causing evaluation failures (8s sleep too short — need 16s), context budget hardcoded at 3000 chars (too small for document uploads), and CacheService missing error handling for Redis failures.",
        "multi_hop", "hard")

    add("What is the relationship between embedding quality and RAG answer quality?",
        f("embedding", "retrieval", "quality", "answer", "recall", "context"),
        "Embedding quality determines retrieval quality, which is the bottleneck for RAG. If the retriever cannot find the relevant document (recall miss), no amount of prompt engineering improves the answer. Notes document that retrieval accuracy gates answer quality — the survey finding confirms this. Higher-quality embeddings enable better semantic similarity matching, and retrieval metrics (Recall@K, MRR) directly predict answer quality.",
        "multi_hop", "hard")

    add("How do I balance study, projects, and personal life as a student?",
        f("study", "productivity", "balance", "health", "burnout", "schedule"),
        "From personal notes: schedule one complete rest day per week (workaholic burnout is real), protect morning hours for deep work (maker schedule), exercise consistently for mood and energy, use Pomodoro for focus, set a phone cutoff time for better sleep, and remember that the project teaches more than any single course. Consistency beats intensity.",
        "multi_hop", "medium")

    # ---- TEMPORAL ----
    add("What tasks and reminders do I have pending?",
        f("deadline", "submit", "due", "pending", "remind", "by", min_match=2)[:8],
        "Based on notes: pay hostel fees before March 31, dentist appointment March 15, capstone progress report due March 25, vehicle insurance renewal before April 10, renew GitHub Student Pack, submit IEEE paper review comments, and check scholarship credit. Multiple bill payments are also pending.",
        "temporal", "medium",
        "Accept any answer listing pending tasks from the notes. Exact list may vary.")

    add("What appointments and scheduled events do I have coming up?",
        f("appointment", "dentist", "doctor", "checkup", "schedule", "booked"),
        "Upcoming appointments from notes: dentist appointment March 15 at 10 AM at Fortis Dental Clinic (bring insurance card), health checkup before semester end, vehicle insurance renewal deadline April 10.",
        "temporal", "easy")

    add("What are my financial obligations this month?",
        f("pay", "bill", "fee", "due", "payment", "electricity", min_match=2),
        "Monthly financial obligations from notes: hostel fees due March 31, electricity bill Rs 1,240 due March 5, internet and water bill payments, Jio recharge needed, mess bill split with roommates. Monthly subscriptions (Netflix, Spotify, ChatGPT Plus) total ~Rs 1,945.",
        "temporal", "medium")

    add("What trips am I planning in the near future?",
        f("trip", "plan", "book", "travel", "train", "ticket", min_match=2),
        "Upcoming travel: Delhi trip for hackathon (train from Chandigarh at 7:10 AM Shatabdi, hackathon at IIT Delhi), home visit for Holi (leave Friday, return Monday), possible Mcleodganj solo trip after exams. Also planning Goa post-placements with friends (budget Rs 8,000 per person).",
        "temporal", "medium")

    # ---- COMPARISON ----
    add("How does Kafka compare to Redis for building a job queue?",
        f("kafka", "redis", "queue", "message", "broker"),
        "Redis is simpler for basic job queues: BRPOPLPUSH provides reliable delivery with an inflight queue, fast setup, already present in most backends. Kafka suits high-throughput event streaming with replay and consumer groups for complex routing. For a personal note processing queue, Redis is the right choice. Kafka adds operational overhead not justified until millions of messages per day.",
        "comparison", "hard")

    add("What are the trade-offs between Python and Go for backend development?",
        f("python", "go", "goroutine", "async"),
        "Python: expressive, huge ecosystem, asyncio for I/O concurrency, GIL limits CPU parallelism — use multiprocessing. Go: goroutines are extremely lightweight (can spawn millions), no GIL, compiled to binary, excellent for CPU-bound and high-concurrency workloads. Python wins for rapid development and ML integration. Go wins for performance-critical services.",
        "comparison", "hard")

    add("Compare LRU and LFU cache eviction policies.",
        f("lru", "lfu", "arc", "cache", "eviction"),
        "LRU (Least Recently Used) evicts the item not accessed for the longest time — good for recency-based access patterns. LFU (Least Frequently Used) evicts the item accessed least often — better for stable hot-set workloads. ARC adapts between LRU and LFU based on hit rates, offering the best of both. Python's OrderedDict implements LRU natively.",
        "comparison", "medium")

    add("Reranking vs hybrid fusion: which approach is better for RAG?",
        f("rerank", "hybrid", "fusion", "rrf", "cross-encoder"),
        "Hybrid fusion (BM25 + dense vectors, combined with RRF or score normalization) improves first-stage recall without extra inference cost. Cross-encoder reranking adds a second precision stage on top of the recall set — higher quality but O(n) per query. The optimal pipeline uses hybrid retrieval for the top-50 candidates followed by cross-encoder reranking to the top-5. RRF is the preferred fusion method as it requires no score calibration.",
        "comparison", "hard")

    add("What are the trade-offs between monolith and microservices architectures?",
        f("microservice", "monolith", "service", "deployment"),
        "Monoliths are simpler to develop, test, and deploy initially — no network latency between components, easier debugging. Microservices enable independent scaling and deployment but add operational complexity (service discovery, distributed tracing, network failures). The pragmatic approach: start with a modular monolith, extract services only when a specific component has materially different scaling requirements.",
        "comparison", "hard")

    # ---- SYNTHESIS ----
    add("Summarize all my AI and machine learning study notes.",
        f("ai", "machine learning", "llm", "embedding", "rag", "transformer", min_match=1)[:10],
        "AI/ML notes cover: RAG architecture (retrieval → context injection → generation), embedding models (all-MiniLM-L6-v2, FAISS, pgvector), LLM evaluation (MRR, Recall, faithfulness, hallucination), prompting techniques (chain-of-thought, few-shot, temperature), fine-tuning methods (LoRA, DPO, instruction tuning), and retrieval strategies (hybrid, reranking, HyDE, query expansion).",
        "synthesis", "hard")

    add("What are all the KnowledgeVault architectural decisions I've documented?",
        f("knowledgevault", "architecture", "decision", "design"),
        "KnowledgeVault architecture decisions: PostgreSQL + pgvector over dedicated vector DB (simplicity), Redis reliable queue (brpoplpush) over plain task queue, deterministic Python category naming (no LLM for naming), hybrid retrieval (semantic + intent), graceful degradation (never returns 500 on LLM failure), Gemini + Groq fallback chain, background worker for async indexing, SHA-256 cache keys with provider signature.",
        "synthesis", "hard")

    add("What programming languages and technologies have I been studying?",
        f("python", "go", "rust", "javascript", "typescript", min_match=1)[:10],
        "Technologies studied: Python (most extensive — async, dataclasses, decorators, generators, typing), JavaScript/TypeScript (Promises, event loop, discriminated unions), Go (goroutines, interfaces, defer, error handling), Rust (ownership, borrowing, Result type), SQL (window functions, CTEs, indexes). Also: FastAPI, PostgreSQL, Redis, Docker, Kubernetes, Terraform.",
        "synthesis", "medium",
        "Accept any answer covering multiple languages with key concepts.")

    add("Summarize my health and wellness notes.",
        f("workout", "sleep", "nutrition", "supplement", "anxiety", "health"),
        "Health notes cover: workout routine (push-pull-legs 3x/week), sleep optimization (20-20-20 rule, 10:30 PM cutoff, 90-minute cycles), nutrition (100g protein/day, Vitamin D deficiency supplement), supplements (D3, Magnesium Glycinate, Omega-3, Zinc), mental health (4-7-8 breathing, morning meditation, journaling), and ergonomics (standing breaks, wrist posture, monitor height).",
        "synthesis", "medium")

    add("What are all my startup ideas and business notes?",
        f("startup", "idea", "business", "saas", "product", "market", min_match=1)[:8],
        "Startup ideas documented: AI-powered study planner for college schedules, hyperlocal campus food delivery, KnowledgeVault as team knowledge management, developer tools SaaS (codebase-trained code reviewer), AI writing assistant for Indian legal documents, AI resume reviewer (Rs 99/review), Indian government data API subscription service. Key frameworks: 1000 true fans, validate with 10 customer conversations before coding.",
        "synthesis", "medium")

    # ---- AMBIGUOUS ----
    add("What have I been learning lately?",
        f("learned", "learning", "studying", "course", "today", min_match=1)[:8],
        "Recent learning covers a wide range: Python advanced patterns (descriptors, generators, async), AI/ML techniques (RAG, reranking, fine-tuning, evaluation metrics), system design (consistent hashing, saga pattern, observability), university subjects (OS scheduling, DBMS normalization, networking), and personal skills (ergonomics, sleep science, productivity techniques).",
        "ambiguous", "medium",
        "Accept any reasonable synthesis of recent study topics.")

    add("What technical problems have I been solving?",
        f("bug", "fix", "error", "debug", "problem", "issue", min_match=2)[:8],
        "Recent technical problems: N+1 SQLAlchemy queries (fixed with joinedload), Redis pool exhaustion under load (increased pool size), race condition in note worker (fixed with brpoplpush reliable queue), Gemini API 429 rate limits during evaluation, memory leak from per-request model loading, category embedding drift causing misclassification.",
        "ambiguous", "medium")

    add("What are the most important things I've realized this month?",
        f("realized", "reflection", "learned", "understand", "insight", min_match=1)[:6],
        "Key realizations: the hybrid retrieval benchmark showed zero improvement over semantic despite the architectural complexity — a lesson in measuring before assuming. Engineering requires honesty about what works. The best engineers are persistent, not necessarily the smartest. Documentation is written for the next reader, not the author.",
        "ambiguous", "hard",
        "Accept any synthesis of journal and learning reflections.")

    add("Notes related to my project",
        f("project", "build", "implement", "feature", "deploy", min_match=1)[:8],
        "Project notes span KnowledgeVault (RAG backend, hybrid retrieval, evaluation framework), capstone project (Timetable Management System for Thapar), hackathon project (AI study planner), and various side project ideas (code review assistant, Indian government data API). KnowledgeVault is the most developed, with the evaluation framework and hybrid retrieval analysis being notable contributions.",
        "ambiguous", "medium")

    # ---- CATEGORY-ORIENTED ----
    add("Show all my communication and meeting notes.",
        f("tell", "message", "sid", "meeting", "sync", "discuss", min_match=1)[:8],
        "Communication notes include messages to Siddhant/Sid about backend meeting, internship opportunity, hackathon registration form, and KnowledgeVault architecture discussions. Meeting notes cover capstone progress meetings with Professor Sharma, team syncs, mentor sessions with Arjun, and hackathon team planning.",
        "category", "easy")

    add("What reminders and shopping lists do I have?",
        f("grocery", "milk", "buy", "shopping", "reminder", "list", min_match=1)[:6],
        "Shopping list includes: milk, bread, eggs, bananas, oats, curd, green tea, maggi, notebook, and pens. Other reminders: return library book by March 20, pay hostel fees before March 31, recharge Jio plan, dentist appointment March 15, renew vehicle insurance before April 10.",
        "category", "easy")

    add("What ideas am I excited about?",
        f("idea", "excited", "startup", "build", "create", "concept", min_match=1)[:6],
        "Exciting ideas include: KnowledgeVault as a team knowledge management product (competing with Confluence but AI-native), AI-powered study planner for college students, developer tools SaaS with codebase-trained code review, Indian government data API subscription service, and open-sourcing KnowledgeVault with a blog post about the hybrid retrieval findings.",
        "category", "easy")

    add("Show all my university study notes.",
        f("university", "lecture", "exam", "professor", "assignment", "thapar", min_match=1)[:8],
        "University study notes cover: OS (scheduling algorithms, page replacement, deadlock conditions, virtual memory), DBMS (normalization, ACID, B+ trees, ER diagrams), Computer Networks (TCP, OSI model, subnetting), Algorithms (dynamic programming, graph algorithms, greedy), and Compiler Design (lexer implementation, DFA, CFG). Capstone project is building a Timetable Management System.",
        "category", "medium")

    # ---- EXACT KEYWORD ----
    add("What is BRPOPLPUSH?",
        f("brpoplpush", "inflight", "reliable queue"),
        "BRPOPLPUSH atomically moves a job from the main queue to an inflight queue in a single operation. This enables reliable at-least-once delivery: if the worker crashes mid-processing, the job stays in the inflight queue and is recovered on worker restart via a startup recovery function. It prevents the silent job loss that occurs with a plain BRPOP.",
        "factual_lookup", "hard")

    add("What is Atomic Habits about?",
        f("atomic habits", "james clear", "habit", "cue", min_match=1),
        "Atomic Habits by James Clear covers habit formation through cue-routine-reward loops. The key insight is that environment design is more powerful than willpower — make good habits obvious, attractive, easy, and satisfying; make bad habits invisible, unattractive, difficult, and unsatisfying. Small 1% improvements compound to remarkable results over time.",
        "factual_lookup", "easy")

    add("What is the walrus operator in Python?",
        f("walrus", ":="),
        "The walrus operator (:=) is Python's assignment expression, introduced in Python 3.8. It assigns a value to a variable as part of an expression. Example: `if (n := len(a)) > 10: print(n)` — this calls len() once and uses the result in both the condition and the body. Useful for avoiding repeated function calls in while loops and comprehensions.",
        "factual_lookup", "easy")

    add("What is CQRS?",
        f("cqrs", "command query", "read model", "write model"),
        "CQRS (Command Query Responsibility Segregation) separates the write model (which accepts commands that change state) from the read model (optimized for querying). This allows each model to be optimized independently and even stored in different databases. It pairs naturally with Event Sourcing, where state changes are stored as events.",
        "factual_lookup", "medium")

    # Filter empty
    entries = [e for e in entries if e.get("expected_note_ids")]
    logger.info("Generated %d ask benchmark entries", len(entries))
    return entries


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--user-id", type=int, default=1)
    parser.add_argument("--output-dir", type=str, default="evaluation_results/benchmarks")
    return parser.parse_args()


def main():
    args = parse_args()
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    db = SessionLocal()
    try:
        notes = load_notes(db, args.user_id)
        logger.info("Loaded %d organized notes for user_id=%d", len(notes), args.user_id)

        if len(notes) < 100:
            logger.warning(
                "Only %d notes loaded. Run ingest_dataset.py first for a meaningful benchmark.",
                len(notes),
            )

        # Reset counters
        RetrievalEntry._counter = 0
        AskEntry._counter = 0

        ret_entries = generate_retrieval_benchmark(notes)
        ask_entries = generate_ask_benchmark(notes)

    finally:
        db.close()

    ret_path = out / "retrieval_benchmark.json"
    ask_path = out / "ask_benchmark.json"

    ret_path.write_text(json.dumps(ret_entries, indent=2))
    ask_path.write_text(json.dumps(ask_entries, indent=2))

    logger.info("Retrieval benchmark: %d queries → %s", len(ret_entries), ret_path)
    logger.info("Ask benchmark:       %d queries → %s", len(ask_entries), ask_path)

    # Coverage report
    type_counts: dict[str, int] = {}
    for e in ret_entries:
        for tag in e.get("tags", []):
            if tag in ("exact", "ambiguous", "comparison", "semantic", "temporal", "multi_hop"):
                type_counts[tag] = type_counts.get(tag, 0) + 1
    # infer from query patterns
    logger.info("Retrieval query summary by difficulty:")
    for diff in ["easy", "medium", "hard"]:
        count = sum(1 for e in ret_entries if e["difficulty"] == diff)
        logger.info("  %s: %d", diff, count)

    ask_cats: dict[str, int] = {}
    for e in ask_entries:
        c = e.get("category", "other")
        ask_cats[c] = ask_cats.get(c, 0) + 1
    logger.info("Ask benchmark categories:")
    for cat, count in sorted(ask_cats.items(), key=lambda x: -x[1]):
        logger.info("  %s: %d", cat, count)


if __name__ == "__main__":
    main()
