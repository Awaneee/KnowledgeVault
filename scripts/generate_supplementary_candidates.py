"""
Supplementary benchmark candidate generator.

Produces ~110 additional candidates targeting gaps in the current 98-entry
verified.json:
  - Paraphrase variants of the 10 most-used original queries
  - Under-represented intent types: meeting, project, general, event
  - Under-represented retrieval challenges: lexical_gap, temporal, comparison
  - Tech-specific reference queries (FastAPI, SQLAlchemy, algorithms, Redis)
  - Additional communication / person-directed queries
  - More question-style knowledge lookup queries
  - Cross-topic synthesis queries

All relevant_note_ids are assigned by keyword matching — auto-approve sets
grades (2 for primary, 1 for secondary).

Outputs to app/evaluation/benchmark/supplementary_candidates.json.
Run human_eval.py --auto-approve on that file to merge into verified.json.
"""

from __future__ import annotations

import hashlib
import json
import logging
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import app.database.base_all  # noqa: F401
from app.database.session import SessionLocal
from app.models.notes import Note
from sqlalchemy.orm import Session

logging.basicConfig(level=logging.WARNING)


def load_notes(db: Session, user_id: int) -> list[tuple[int, str, str]]:
    rows = (
        db.query(Note.id, Note.title, Note.content)
        .filter(Note.user_id == user_id, Note.organization_status == "organized")
        .order_by(Note.id)
        .all()
    )
    return [(r.id, r.title or "", r.content or "") for r in rows]


def find(notes, *keywords, min_match=1, cap=8):
    kws = [k.lower() for k in keywords]
    matched = []
    for nid, title, content in notes:
        text = (title + " " + content).lower()
        if sum(1 for k in kws if k in text) >= min_match:
            matched.append(nid)
    return matched[:cap]


def find_exact(notes, phrase):
    pl = phrase.lower()
    return [nid for nid, t, c in notes if pl in (t + " " + c).lower()]


def stable_id(primary_nid: int, qtype: str, query: str) -> str:
    digest = hashlib.sha256(query.encode()).hexdigest()[:6]
    return f"{primary_nid}_{qtype}_{digest}"


def entry(primary_nid, query, ids, intent, category, difficulty="medium",
          tags=None, challenge=None, qtype="tp"):
    if not ids:
        return None
    pid = primary_nid if primary_nid in ids else ids[0]
    return {
        "id": stable_id(pid, qtype, query),
        "query": query,
        "expected_intent": intent,
        "expected_category": category,
        "relevant_note_ids": ids[:8],
        "difficulty": difficulty,
        "tags": tags or [],
        "retrieval_challenge": challenge,
        "graded_relevance": None,
        "labeling_notes": "",
        "labeled_at": None,
    }


def generate(notes) -> list[dict]:
    E = entry
    f = lambda *kws, **kwargs: find(notes, *kws, **kwargs)
    fx = lambda phrase: find_exact(notes, phrase)
    out = []

    def add(*args, **kwargs):
        e = E(*args, **kwargs)
        if e:
            out.append(e)

    # ── Paraphrase variants of top original queries ──────────────────────

    sid_ids = f("sid", "siddhant", min_match=1)
    if sid_ids:
        add(sid_ids[0], "Messages I need to send Siddhant", sid_ids, "communication", "Things to Tell Sid", "easy", ["sid", "paraphrase"], "lexical_gap", "tp")
        add(sid_ids[0], "Pending conversations with Sid", sid_ids, "communication", "Things to Tell Sid", "easy", ["sid", "paraphrase"], "semantic", "tp")
        add(sid_ids[0], "Notes about Sid and our project discussions", sid_ids, "communication", "Things to Tell Sid", "medium", ["sid"], "semantic", "tp")

    startup_ids = f("startup", "idea", "business", min_match=1)
    if startup_ids:
        add(startup_ids[0], "Business concepts I want to explore", startup_ids, "idea", "Ideas", "easy", ["startup", "paraphrase"], "semantic", "tp")
        add(startup_ids[0], "Product ideas I have noted down", startup_ids, "idea", "Ideas", "easy", ["idea", "paraphrase"], "semantic", "tp")
        add(startup_ids[0], "Entrepreneurship and venture ideas", startup_ids, "idea", "Ideas", "medium", ["startup"], "lexical_gap", "tp")

    bill_ids = f("bill", "pay", "fee", "rent", min_match=1)
    if bill_ids:
        add(bill_ids[0], "Outstanding financial obligations", bill_ids, "todo", "Bills", "medium", ["bills", "paraphrase"], "lexical_gap", "tp")
        add(bill_ids[0], "Payments I still need to make", bill_ids, "todo", "Bills", "easy", ["bills"], "semantic", "tp")
        add(bill_ids[0], "Monthly expenses and dues", bill_ids, "todo", "Bills", "medium", ["finance"], "semantic", "tp")

    health_ids = f("doctor", "appointment", "health", "checkup", min_match=1)
    if health_ids:
        add(health_ids[0], "Medical appointments on my calendar", health_ids, "todo", "To Do", "easy", ["health", "paraphrase"], "semantic", "tp")
        add(health_ids[0], "Healthcare and wellness reminders", health_ids, "reminder", "Appointments", "easy", ["health"], "lexical_gap", "tp")

    redis_ids = f("redis", "eviction", "lru", min_match=1)
    if redis_ids:
        add(redis_ids[0], "In-memory datastore behavior notes", redis_ids, "study", "Study - Redis", "medium", ["redis", "paraphrase"], "lexical_gap", "tp")
        add(redis_ids[0], "Cache eviction policy details", redis_ids, "study", "Study - Redis", "medium", ["redis"], "semantic", "tp")

    meeting_ids = f("meeting", "sync", "standup", "sprint", min_match=1)
    if meeting_ids:
        add(meeting_ids[0], "Team meetings I have attended", meeting_ids, "event", "Meetings", "easy", ["meeting", "paraphrase"], "semantic", "tp")
        add(meeting_ids[0], "Sprint retrospective and planning notes", meeting_ids, "event", "Meetings", "easy", ["meeting"], "lexical_gap", "tp")
        add(meeting_ids[0], "Sync notes with the team", meeting_ids, "meeting", "Meetings", "easy", ["meeting"], "semantic", "tp")
        add(meeting_ids[0], "Weekly standup summaries", meeting_ids, "meeting", "Meetings", "easy", ["meeting"], "semantic", "tp")

    # ── Under-represented intent types ────────────────────────────────────

    # project
    kv_ids = f("knowledgevault", "knowledge vault", min_match=1)
    if kv_ids:
        add(kv_ids[0], "KnowledgeVault project milestones and deliverables", kv_ids, "project", "Projects", "medium", ["project"], "semantic", "tp")
        add(kv_ids[0], "What is the architecture of my main project?", kv_ids, "project", "Projects", "hard", ["project"], "multi_hop", "tp")
        add(kv_ids[0], "Current sprint goals for KnowledgeVault", kv_ids, "project", "Projects", "medium", ["project", "sprint"], "semantic", "tp")

    capstone_ids = f("capstone", "thapar", "college", "university", min_match=1)
    if capstone_ids:
        add(capstone_ids[0], "Capstone project tasks and status", capstone_ids, "project", "Projects", "medium", ["capstone", "project"], "semantic", "tp")
        add(capstone_ids[0], "University project submission deadlines", capstone_ids, "project", "Projects", "easy", ["capstone"], "semantic", "tp")

    # general / reflection
    journal_ids = f("today", "reflection", "feeling", "grateful", "goal", min_match=1)
    if journal_ids:
        add(journal_ids[0], "My personal reflections and journal entries", journal_ids[:6], "general", "General", "easy", ["journal"], "semantic", "tp")
        add(journal_ids[0], "What did I realize recently?", journal_ids[:6], "general", "General", "hard", ["journal", "reflection"], "semantic", "tp")
        add(journal_ids[0], "Insights I've been writing down", journal_ids[:6], "general", "General", "medium", ["journal"], "lexical_gap", "tp")

    career_ids = f("career", "backend", "engineer", "senior", "google", min_match=1)
    if career_ids:
        add(career_ids[0], "My career goals and direction notes", career_ids, "general", "General", "medium", ["career"], "semantic", "tp")
        add(career_ids[0], "Long-term professional planning notes", career_ids, "general", "General", "hard", ["career"], "lexical_gap", "tp")

    productivity_ids = f("productivity", "pomodoro", "focus", "distraction", min_match=1)
    if productivity_ids:
        add(productivity_ids[0], "Time management and focus techniques", productivity_ids, "reference", "Reference - Productivity", "easy", ["productivity"], "semantic", "tp")
        add(productivity_ids[0], "Notes on staying productive while studying", productivity_ids, "reference", "Reference - Productivity", "medium", ["productivity"], "lexical_gap", "tp")

    # ── Tech reference queries ────────────────────────────────────────────

    fastapi_ids = f("fastapi", "dependency", "router", "pydantic", min_match=1)
    if fastapi_ids:
        add(fastapi_ids[0], "FastAPI route and dependency injection notes", fastapi_ids, "reference", "Reference - KnowledgeVault Backend", "medium", ["fastapi"], "semantic", "tp")
        add(fastapi_ids[0], "Python web framework notes for FastAPI", fastapi_ids, "study", "Study - FastAPI", "easy", ["fastapi"], "lexical_gap", "tp")
        add(fastapi_ids[0], "API endpoint design patterns in FastAPI", fastapi_ids, "reference", "Reference - KnowledgeVault Backend", "medium", ["fastapi", "api"], "semantic", "tp")

    sqlalchemy_ids = f("sqlalchemy", "orm", "session", "query", "joinedload", min_match=1)
    if sqlalchemy_ids:
        add(sqlalchemy_ids[0], "SQLAlchemy ORM usage patterns", sqlalchemy_ids, "reference", "Reference - KnowledgeVault Backend", "medium", ["sqlalchemy"], "lexical", "tp")
        add(sqlalchemy_ids[0], "Database session management in Python", sqlalchemy_ids, "study", "Study - FastAPI", "medium", ["sqlalchemy", "db"], "semantic", "tp")
        add(sqlalchemy_ids[0], "How do I fix N+1 query problems?", sqlalchemy_ids, "question", "Questions", "hard", ["sqlalchemy", "n1"], "semantic", "tp")

    pgvector_ids = f("pgvector", "hnsw", "ivfflat", "vector", "cosine", min_match=2)
    if pgvector_ids:
        add(pgvector_ids[0], "pgvector setup and index configuration", pgvector_ids, "reference", "Reference - PostgreSQL", "hard", ["pgvector", "vector"], "lexical", "tp")
        add(pgvector_ids[0], "Vector similarity search configuration", pgvector_ids, "study", "Study - AI", "hard", ["pgvector", "vectors"], "semantic", "tp")

    algo_ids = f("algorithm", "binary search", "graph", "dynamic programming", "sorting", min_match=1)
    if algo_ids:
        add(algo_ids[0], "Algorithm and data structure study notes", algo_ids, "study", "Study - Algorithms", "medium", ["algorithms", "dsa"], "lexical", "tp")
        add(algo_ids[0], "Competitive programming problem patterns", algo_ids, "study", "Study - Algorithms", "hard", ["algorithms"], "semantic", "tp")
        add(algo_ids[0], "How do I solve graph traversal problems?", algo_ids, "question", "Questions", "medium", ["algorithms", "graph"], "semantic", "tp")

    os_ids = f("operating system", "scheduling", "process", "thread", "deadlock", min_match=1)
    if os_ids:
        add(os_ids[0], "Operating systems exam preparation notes", os_ids, "study", "Study - Operating Systems", "medium", ["os", "university"], "semantic", "tp")
        add(os_ids[0], "CPU scheduling algorithms I need to know", os_ids, "study", "Study - Operating Systems", "medium", ["os"], "semantic", "tp")

    network_ids = f("tcp", "osi", "subnet", "network", "http", "dns", min_match=1)
    if network_ids:
        add(network_ids[0], "Computer networking concepts for university", network_ids, "study", "Study - Computer Networks", "medium", ["networking", "university"], "lexical", "tp")
        add(network_ids[0], "TCP/IP and HTTP protocol notes", network_ids, "study", "Study - Computer Networks", "easy", ["networking"], "lexical", "tp")

    kubernetes_ids = f("kubernetes", "k8s", "pod", "deployment", min_match=1)
    if kubernetes_ids:
        add(kubernetes_ids[0], "Kubernetes cluster management notes", kubernetes_ids, "study", "Study - Kubernetes", "medium", ["kubernetes"], "lexical", "tp")
        add(kubernetes_ids[0], "Container orchestration with K8s", kubernetes_ids, "study", "Study - Kubernetes", "hard", ["kubernetes"], "lexical_gap", "tp")

    auth_ids = f("oauth", "jwt", "auth", "token", "bearer", min_match=1)
    if auth_ids:
        add(auth_ids[0], "Authentication and JWT token notes", auth_ids, "study", "Study - Security", "medium", ["auth", "jwt"], "lexical", "tp")
        add(auth_ids[0], "How does OAuth 2.0 work?", auth_ids, "question", "Questions", "medium", ["auth", "oauth"], "semantic", "tp")

    # ── Question-style knowledge lookup ──────────────────────────────────

    redis_evict_ids = f("redis", "eviction", "lru", "memory", min_match=1)
    if redis_evict_ids:
        add(redis_evict_ids[0], "What eviction policies does Redis support?", redis_evict_ids, "question", "Questions", "medium", ["redis", "eviction"], "semantic", "tp")

    postgres_idx_ids = f("postgresql", "index", "b-tree", "gin", "hnsw", min_match=1)
    if postgres_idx_ids:
        add(postgres_idx_ids[0], "What types of indexes does PostgreSQL support?", postgres_idx_ids, "question", "Questions", "medium", ["postgres", "index"], "semantic", "tp")
        add(postgres_idx_ids[0], "When should I use GIN vs B-tree indexes?", postgres_idx_ids, "question", "Questions", "hard", ["postgres", "index"], "comparison", "tp")

    rag_ids = f("rag", "retrieval-augmented", "retrieval augmented", min_match=1)
    if rag_ids:
        add(rag_ids[0], "How does retrieval augmented generation work?", rag_ids, "question", "Questions", "medium", ["rag", "ai"], "semantic", "tp")
        add(rag_ids[0], "What are the steps in a RAG pipeline?", rag_ids, "question", "Questions", "hard", ["rag"], "semantic", "tp")

    embed_ids = f("embedding", "vector", "semantic", "cosine", min_match=2)
    if embed_ids:
        add(embed_ids[0], "How are text embeddings generated?", embed_ids, "question", "Questions", "medium", ["embeddings"], "semantic", "tp")
        add(embed_ids[0], "What is the difference between semantic and keyword search?", embed_ids, "question", "Questions", "hard", ["embeddings", "search"], "semantic", "tp")

    # ── Temporal queries ──────────────────────────────────────────────────

    deadline_ids = f("deadline", "due", "by", "before", "submit", min_match=2)
    if deadline_ids:
        add(deadline_ids[0], "What is due this week?", deadline_ids[:6], "todo", "Tasks", "medium", ["temporal", "deadline"], "temporal", "tp")
        add(deadline_ids[0], "Upcoming deadlines and submission dates", deadline_ids[:6], "todo", "Tasks", "medium", ["temporal"], "temporal", "tp")
        add(deadline_ids[0], "Tasks I need to complete before month end", deadline_ids[:6], "todo", "Tasks", "hard", ["temporal"], "temporal", "tp")

    appt_ids = f("appointment", "scheduled", "dentist", "doctor", "booked", min_match=1)
    if appt_ids:
        add(appt_ids[0], "What appointments have I booked this month?", appt_ids, "reminder", "Appointments", "medium", ["temporal", "appointment"], "temporal", "tp")

    trip_ids = f("trip", "travel", "train", "flight", "book", min_match=1)
    if trip_ids:
        add(trip_ids[0], "My upcoming travel and trip bookings", trip_ids, "todo", "Travel", "easy", ["travel", "temporal"], "temporal", "tp")
        add(trip_ids[0], "Transport and accommodation I need to arrange", trip_ids, "todo", "Travel", "medium", ["travel"], "lexical_gap", "tp")

    # ── Comparison / multi-hop queries ────────────────────────────────────

    redis_pg_ids = list(set(f("redis", min_match=1)[:4]) | set(f("postgresql", "postgres", min_match=1)[:4]))
    if redis_pg_ids:
        add(redis_pg_ids[0], "Redis vs PostgreSQL — when to use each for persistence?", redis_pg_ids, "study", "Study - System Design", "hard", ["comparison", "redis", "postgres"], "comparison", "tp")

    docker_k8s_ids = list(set(f("docker", "container", min_match=1)[:4]) | set(f("kubernetes", "k8s", min_match=1)[:4]))
    if docker_k8s_ids:
        add(docker_k8s_ids[0], "Docker vs Kubernetes — what is the difference?", docker_k8s_ids, "study", "Study - System Design", "hard", ["comparison", "docker", "kubernetes"], "comparison", "tp")

    rag_rerank_ids = list(set(f("rag", "retrieval", min_match=1)[:4]) | set(f("rerank", "cross-encoder", min_match=1)[:4]))
    if rag_rerank_ids:
        add(rag_rerank_ids[0], "How do I decide between hybrid retrieval and cross-encoder reranking?", rag_rerank_ids, "study", "Study - AI", "hard", ["comparison", "rag", "reranking"], "multi_hop", "tp")

    kv_eval_ids = list(set(kv_ids[:4]) | set(f("evaluation", "benchmark", "mrr", "recall", min_match=2)[:4]))
    if kv_eval_ids:
        add(kv_eval_ids[0], "What have I documented about retrieval quality in KnowledgeVault?", kv_eval_ids, "reference", "Reference - KnowledgeVault", "hard", ["multi_hop", "evaluation"], "multi_hop", "tp")

    # ── Synthesis / category browsing ────────────────────────────────────

    all_study_ids = f("study", "revision", "exam", "learn", min_match=1)
    if all_study_ids:
        add(all_study_ids[0], "All my university and course study notes", all_study_ids[:8], "study", "Study Tasks", "easy", ["synthesis", "study"], "synthesis", "tp")

    all_idea_ids = f("idea", "brainstorm", "concept", min_match=1)
    if all_idea_ids:
        add(all_idea_ids[0], "All my brainstorming and ideation notes", all_idea_ids[:8], "idea", "Ideas", "easy", ["synthesis", "idea"], "synthesis", "tp")

    all_ref_ids = f("reference", "cheat sheet", "cheatsheet", min_match=1)
    if all_ref_ids:
        add(all_ref_ids[0], "My technical reference cheat sheets", all_ref_ids[:6], "reference", "Reference Notes", "easy", ["synthesis", "reference"], "synthesis", "tp")

    all_comm_ids = f("tell", "message", "email", "discuss", "communicate", min_match=1)
    if all_comm_ids:
        add(all_comm_ids[0], "All my communication and message drafts", all_comm_ids[:6], "communication", "Communication", "easy", ["synthesis", "communication"], "synthesis", "tp")

    # ── Lexical gap queries (user phrase vs note phrasing differ) ─────────

    grocery_ids = f("grocery", "milk", "eggs", "bread", "buy", min_match=1)
    if grocery_ids:
        add(grocery_ids[0], "Errands I need to run today", grocery_ids, "todo", "To Do", "medium", ["lexical_gap", "shopping"], "lexical_gap", "tp")
        add(grocery_ids[0], "Things I need to pick up from the store", grocery_ids, "todo", "Shopping", "easy", ["shopping"], "lexical_gap", "tp")

    workout_ids = f("workout", "exercise", "gym", "fitness", min_match=1)
    if workout_ids:
        add(workout_ids[0], "Physical training and exercise plan", workout_ids, "todo", "Health", "easy", ["health", "fitness"], "lexical_gap", "tp")
        add(workout_ids[0], "How am I planning to stay healthy?", workout_ids, "question", "Questions", "medium", ["health"], "semantic", "tp")

    budget_ids = f("budget", "spending", "expense", "monthly", min_match=1)
    if budget_ids:
        add(budget_ids[0], "How much am I spending per month?", budget_ids, "question", "Questions", "medium", ["finance", "budget"], "semantic", "tp")
        add(budget_ids[0], "Personal finance tracking notes", budget_ids, "reference", "Finance", "easy", ["finance"], "semantic", "tp")

    # ── Additional exact phrase queries ──────────────────────────────────

    brpoplpush_ids = fx("brpoplpush")
    if brpoplpush_ids:
        add(brpoplpush_ids[0], "BRPOPLPUSH reliable queue implementation", brpoplpush_ids, "reference", "Reference - Redis", "hard", ["redis", "exact_phrase"], "exact_phrase", "tp")

    acid_ids = fx("ACID")
    if acid_ids:
        add(acid_ids[0], "ACID properties of databases", acid_ids, "study", "Study - DBMS", "easy", ["database", "acid", "exact_phrase"], "exact_phrase", "tp")

    rrf_ids = fx("Reciprocal Rank Fusion")
    if not rrf_ids:
        rrf_ids = fx("rrf")
    if rrf_ids:
        add(rrf_ids[0], "RRF score combination for hybrid search", rrf_ids, "study", "Study - AI", "hard", ["rag", "rrf"], "exact_phrase", "tp")

    hnsw_ids = fx("HNSW")
    if hnsw_ids:
        add(hnsw_ids[0], "HNSW approximate nearest neighbor algorithm", hnsw_ids, "study", "Study - AI", "hard", ["vectors", "hnsw"], "exact_phrase", "tp")

    # ── Shopping and reminders ────────────────────────────────────────────

    shopping_ids = f("grocery", "milk", "bread", "buy", "shopping", min_match=1)
    if shopping_ids:
        add(shopping_ids[0], "What do I need to buy this weekend?", shopping_ids, "todo", "Shopping", "easy", ["shopping", "reminder"], "semantic", "tp")

    remind_ids = f("remind", "reminder", "don't forget", "remember", min_match=1)
    if remind_ids:
        add(remind_ids[0], "All my pending reminders and follow-ups", remind_ids[:6], "reminder", "Reminders", "easy", ["reminder"], "semantic", "tp")
        add(remind_ids[0], "What have I told myself not to forget?", remind_ids[:6], "reminder", "Reminders", "medium", ["reminder"], "lexical_gap", "tp")

    # ── Interview prep ────────────────────────────────────────────────────

    leetcode_ids = f("leetcode", "binary search", "sliding window", "two pointer", min_match=1)
    if leetcode_ids:
        add(leetcode_ids[0], "LeetCode patterns and problem-solving techniques", leetcode_ids, "study", "Study - Interview Prep", "medium", ["leetcode", "interview"], "lexical", "tp")
        add(leetcode_ids[0], "How do I approach dynamic programming questions?", leetcode_ids, "question", "Questions", "hard", ["dp", "interview"], "semantic", "tp")

    sysdesign_ids = f("system design", "url shortener", "rate limiter", "consistent hashing", min_match=1)
    if sysdesign_ids:
        add(sysdesign_ids[0], "System design concepts I need to review", sysdesign_ids, "study", "Study - System Design", "medium", ["system_design"], "semantic", "tp")
        add(sysdesign_ids[0], "How do I design a scalable URL shortener?", sysdesign_ids, "question", "Questions", "hard", ["system_design", "interview"], "semantic", "tp")

    behavioral_ids = f("behavioral", "star", "leadership", "conflict", "amazon", min_match=1)
    if behavioral_ids:
        add(behavioral_ids[0], "Behavioral interview story preparation", behavioral_ids, "study", "Study - Interview Prep", "medium", ["behavioral", "interview"], "lexical", "tp")

    resume_ids = f("resume", "cv", "quantify", "bullet point", min_match=1)
    if resume_ids:
        add(resume_ids[0], "Resume writing tips and improvement notes", resume_ids, "reference", "Reference - Career", "easy", ["resume"], "lexical", "tp")
        add(resume_ids[0], "How should I write my software engineer resume?", resume_ids, "question", "Questions", "easy", ["resume", "career"], "semantic", "tp")

    # ── Books and learning resources ──────────────────────────────────────

    book_ids = f("book", "reading", "author", "chapter", "recommended", min_match=1)
    if book_ids:
        add(book_ids[0], "Books I am reading or have read recently", book_ids, "reference", "Reference - Books", "easy", ["books"], "semantic", "tp")
        add(book_ids[0], "Reading list and book notes", book_ids, "reference", "Reference - Books", "easy", ["books"], "lexical", "tp")

    atomic_ids = f("atomic habits", "james clear", "habit", "cue", "routine", min_match=1)
    if atomic_ids:
        add(atomic_ids[0], "Habit formation notes from Atomic Habits", atomic_ids, "study", "Study - Books", "easy", ["books", "habits"], "lexical", "tp")
        add(atomic_ids[0], "Summary of James Clear's key ideas on habits", atomic_ids, "study", "Study - Books", "medium", ["books"], "lexical_gap", "tp")

    course_ids = f("course", "udemy", "tutorial", "cs50", "completed", min_match=1)
    if course_ids:
        add(course_ids[0], "Online courses and tutorials I am taking", course_ids, "study", "Study - Learning", "easy", ["courses"], "semantic", "tp")

    # ── Health and wellness ───────────────────────────────────────────────

    sleep_ids = f("sleep", "melatonin", "circadian", "sleep cycle", min_match=1)
    if sleep_ids:
        add(sleep_ids[0], "Sleep improvement techniques and tips", sleep_ids, "reference", "Reference - Health", "medium", ["sleep", "health"], "lexical", "tp")
        add(sleep_ids[0], "How can I improve my sleep quality?", sleep_ids, "question", "Questions", "medium", ["sleep"], "semantic", "tp")

    nutrition_ids = f("nutrition", "protein", "diet", "vitamin", "supplement", min_match=1)
    if nutrition_ids:
        add(nutrition_ids[0], "Nutrition and supplement tracking notes", nutrition_ids, "reference", "Reference - Health", "easy", ["nutrition"], "semantic", "tp")
        add(nutrition_ids[0], "What supplements should I be taking?", nutrition_ids, "question", "Questions", "medium", ["nutrition", "health"], "semantic", "tp")

    mental_ids = f("anxiety", "meditation", "mindfulness", "mental health", "stress", min_match=1)
    if mental_ids:
        add(mental_ids[0], "Mental health practices and coping strategies", mental_ids, "reference", "Reference - Health", "medium", ["mental_health"], "semantic", "tp")
        add(mental_ids[0], "My notes on managing stress and anxiety", mental_ids, "reference", "Reference - Health", "medium", ["mental_health"], "semantic", "tp")

    # ── Open source / blog / personal brand ──────────────────────────────

    opensource_ids = f("open source", "github", "blog", "build in public", min_match=1)
    if opensource_ids:
        add(opensource_ids[0], "Plans for open source and public building", opensource_ids, "idea", "Ideas", "medium", ["open_source", "blog"], "semantic", "tp")
        add(opensource_ids[0], "Notes on growing my developer presence online", opensource_ids, "idea", "Ideas", "medium", ["personal_brand"], "lexical_gap", "tp")

    # ── Negative queries (no matching notes expected) ─────────────────────

    negatives = [
        ("Fortran programming and legacy code notes", ["fortran", "cobol"]),
        ("Ancient history and archaeology notes", ["history", "archaeology"]),
        ("Wine and cheese pairing recommendations", ["food", "wine"]),
        ("Piano lessons and music theory notes", ["music", "piano"]),
        ("Gardening and plant care notes", ["gardening", "plants"]),
    ]
    for q, tags in negatives:
        out.append({
            "id": stable_id(0, "tp", q),
            "query": q,
            "expected_intent": "general",
            "expected_category": "General",
            "relevant_note_ids": [],
            "difficulty": "hard",
            "tags": tags + ["negative"],
            "retrieval_challenge": "negative",
            "graded_relevance": None,
            "labeling_notes": "",
            "labeled_at": None,
        })

    return [e for e in out if e is not None]


def main():
    db = SessionLocal()
    try:
        notes = load_notes(db, user_id=1)
        print(f"Loaded {len(notes)} notes.")
    finally:
        db.close()

    candidates = generate(notes)

    # Load verified.json to exclude already-reviewed IDs
    verified_path = ROOT / "app" / "evaluation" / "benchmark" / "verified.json"
    existing_ids: set[str] = set()
    if verified_path.exists():
        import json
        existing = json.loads(verified_path.read_text(encoding="utf-8"))
        existing_ids = {e["id"] for e in existing}

    # Also load candidates.json to exclude already-generated IDs
    cands_path = ROOT / "app" / "evaluation" / "benchmark" / "candidates.json"
    if cands_path.exists():
        import json
        existing_cands = json.loads(cands_path.read_text(encoding="utf-8"))
        existing_ids.update(e["id"] for e in existing_cands)

    new_candidates = [c for c in candidates if c["id"] not in existing_ids]

    out_path = ROOT / "app" / "evaluation" / "benchmark" / "supplementary_candidates.json"
    import json
    out_path.write_text(json.dumps(new_candidates, indent=2), encoding="utf-8")
    print(f"Supplementary candidates: {len(new_candidates)} new entries -> {out_path}")

    # Distribution summary
    from collections import Counter
    diffs = Counter(c["difficulty"] for c in new_candidates)
    intents = Counter(c["expected_intent"] for c in new_candidates)
    challenges = Counter(c.get("retrieval_challenge") or "untagged" for c in new_candidates)
    print(f"Difficulty: {dict(sorted(diffs.items()))}")
    print(f"Intent:     {dict(sorted(intents.items()))}")
    print(f"Challenge:  {dict(sorted(challenges.items()))}")


if __name__ == "__main__":
    main()
