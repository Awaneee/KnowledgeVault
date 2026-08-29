#!/usr/bin/env python3
"""
KnowledgeVault Live Smoke Test
==============================
Tests the running backend end-to-end:
  Phase 1 — Note creation + AI intent categorization accuracy
  Phase 2 — Ask AI (single-turn RAG)
  Phase 3 — Multi-turn Chat

Usage:
    python tests/live_smoke_test.py

Env vars (optional overrides):
    KV_BASE_URL   default: http://localhost:8000
    KV_EMAIL      default: ab@gmail.com
    KV_PASSWORD   default: abcdefgh
    KV_CLEANUP    set to "0" to keep test notes for inspection
"""

import os
import sys
import time
from dataclasses import dataclass
from typing import Optional

import requests

# ── Config ────────────────────────────────────────────────────────────────────

BASE_URL   = os.getenv("KV_BASE_URL",  "http://localhost:8000")
EMAIL      = os.getenv("KV_EMAIL",     "ab@gmail.com")
PASSWORD   = os.getenv("KV_PASSWORD",  "abcdefgh")
DO_CLEANUP = os.getenv("KV_CLEANUP",   "1") != "0"

INTENT_TIMEOUT_S = 120  # max wait for AI to assign intent to a note (worker is serial ~2s each)
INTENT_POLL_S    = 2    # polling interval

# ANSI colours
G = "\033[92m"; R = "\033[91m"; Y = "\033[93m"; C = "\033[96m"
B = "\033[1m";  RESET = "\033[0m"

# ── Test data ─────────────────────────────────────────────────────────────────

@dataclass
class NoteCase:
    content: str
    expected: str   # expected intent_type
    label: str      # short description shown in report


NOTE_CASES: list[NoteCase] = [
    # One representative note per intent type (keeps test fast under rate limits)
    NoteCase("submit the assignment by Friday 5pm",                  "todo",          "deadline task"),
    NoteCase("read about transformer architecture in deep learning", "study",         "ML reading"),
    NoteCase("why does my code throw a null pointer exception?",     "question",      "debug question"),
    NoteCase("ask John about the meeting schedule for next week",    "communication", "team ask"),
    NoteCase("take medicine at 8pm every night",                     "reminder",      "health reminder"),
    NoteCase("build a chrome extension for managing browser tabs",   "idea",          "product idea"),
    NoteCase("git stash saves uncommitted changes, git stash pop restores them", "reference", "git ref"),
    NoteCase("AI conference on September 15th in Bangalore",         "event",         "conference"),
]


ASK_QUESTIONS = [
    "What tasks do I need to complete?",
    "What topics am I currently studying?",
    "What events or meetings do I have coming up?",
    "Who do I need to contact or communicate with?",
]

CHAT_TURNS = [
    "What are my pending tasks?",
    "Which of those sounds most urgent?",
    "And what about things I'm studying — give me a summary.",
]


# ── API client ────────────────────────────────────────────────────────────────

class KVClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers["Content-Type"] = "application/json"

    def login(self, email: str, password: str) -> bool:
        r = self.session.post(f"{BASE_URL}/auth/login",
                              json={"email": email, "password": password},
                              timeout=10)
        if r.status_code != 200:
            return False
        self.session.headers["Authorization"] = f"Bearer {r.json()['access_token']}"
        return True

    def create_note(self, content: str) -> Optional[dict]:
        r = self.session.post(f"{BASE_URL}/notes/",
                              json={"content": content}, timeout=15)
        return r.json() if r.status_code == 201 else None

    def delete_note(self, note_id: int):
        self.session.delete(f"{BASE_URL}/notes/{note_id}", timeout=10)

    def get_intent(self, note_id: int) -> Optional[dict]:
        try:
            r = self.session.get(f"{BASE_URL}/intents/notes/{note_id}", timeout=30)
            return r.json() if r.status_code == 200 else None
        except requests.exceptions.Timeout:
            return None
        except requests.exceptions.ConnectionError:
            return None

    def wait_for_intent(self, note_id: int) -> Optional[dict]:
        deadline = time.time() + INTENT_TIMEOUT_S
        while time.time() < deadline:
            intent = self.get_intent(note_id)
            if intent:
                return intent
            time.sleep(INTENT_POLL_S)
        return None

    def wait_for_all_intents(self, note_ids: list) -> dict:
        """Poll all notes concurrently until all assigned or timeout."""
        results = {nid: None for nid in note_ids}
        pending = set(note_ids)
        deadline = time.time() + INTENT_TIMEOUT_S
        while pending and time.time() < deadline:
            for nid in list(pending):
                intent = self.get_intent(nid)
                if intent:
                    results[nid] = intent
                    pending.discard(nid)
            if pending:
                time.sleep(INTENT_POLL_S)
        return results

    def ask(self, question: str) -> Optional[dict]:
        r = self.session.post(f"{BASE_URL}/ask/",
                              json={"question": question}, timeout=120)
        return r.json() if r.status_code == 200 else None

    def create_conversation(self) -> Optional[int]:
        r = self.session.post(f"{BASE_URL}/conversations/", timeout=10)
        return r.json()["id"] if r.status_code == 201 else None

    def chat(self, session_id: int, question: str) -> Optional[dict]:
        r = self.session.post(
            f"{BASE_URL}/conversations/{session_id}/ask",
            json={"question": question},
            timeout=120,
        )
        return r.json() if r.status_code == 200 else None

    def delete_conversation(self, session_id: int):
        self.session.delete(f"{BASE_URL}/conversations/{session_id}", timeout=10)


# ── Printers ──────────────────────────────────────────────────────────────────

def ok(msg):   print(f"  {G}✓{RESET} {msg}")
def bad(msg):  print(f"  {R}✗{RESET} {msg}")
def info(msg): print(f"  {C}→{RESET} {msg}")
def warn(msg): print(f"  {Y}!{RESET} {msg}")
def header(t): print(f"\n{B}{t}{RESET}\n{'─'*64}")


# ── Phase 1: Categorization ───────────────────────────────────────────────────

@dataclass
class CatResult:
    case: NoteCase
    actual: Optional[str]
    confidence: Optional[float]
    note_id: Optional[int]
    timed_out: bool = False

    @property
    def passed(self) -> bool:
        return self.actual == self.case.expected


def phase1_categorization(client: KVClient) -> list[CatResult]:
    header("PHASE 1 — Note Creation + AI Categorization")

    info(f"Creating {len(NOTE_CASES)} test notes...")
    created: list[tuple[NoteCase, Optional[int]]] = []
    for case in NOTE_CASES:
        note = client.create_note(case.content)
        if note:
            created.append((case, note["id"]))
        else:
            bad(f"Failed to create: {case.label}")
            created.append((case, None))

    n_created = sum(1 for _, nid in created if nid)
    ok(f"Created {n_created} notes")
    print(f"\n  Batch-polling for AI intent detection (up to {INTENT_TIMEOUT_S}s total)...\n")

    valid_ids = [nid for _, nid in created if nid]
    intents = client.wait_for_all_intents(valid_ids)

    results: list[CatResult] = []
    for case, note_id in created:
        if note_id is None:
            results.append(CatResult(case=case, actual=None,
                                     confidence=None, note_id=None))
            continue

        intent = intents.get(note_id)
        if intent is None:
            warn(f"TIMEOUT  {case.label:35s}  expected={case.expected}")
            results.append(CatResult(case=case, actual=None,
                                     confidence=None, note_id=note_id,
                                     timed_out=True))
            continue

        actual     = intent.get("intent_type", "?")
        confidence = intent.get("confidence", 0.0)
        passed     = actual == case.expected

        line = (f"{case.label:35s}  "
                f"expected={case.expected:15s}  "
                f"got={actual:15s}  "
                f"conf={confidence:.0%}")
        ok(line) if passed else bad(line)

        results.append(CatResult(case=case, actual=actual,
                                  confidence=confidence, note_id=note_id))
    return results


# ── Phase 2: Ask AI ───────────────────────────────────────────────────────────

def phase2_ask(client: KVClient):
    header("PHASE 2 — Ask AI (single-turn RAG)")
    for q in ASK_QUESTIONS:
        info(f"Q: {q}")
        t0 = time.time()
        resp = client.ask(q)
        elapsed = time.time() - t0
        if resp and resp.get("answer"):
            preview  = resp["answer"][:220].replace("\n", " ")
            n_sources = len(resp.get("sources", []))
            ok(f"({elapsed:.1f}s, {n_sources} sources) {preview}…")
        else:
            bad(f"No answer returned in {elapsed:.1f}s")
        print()


# ── Phase 3: Chat ─────────────────────────────────────────────────────────────

def phase3_chat(client: KVClient):
    header("PHASE 3 — Multi-turn Chat")
    session_id = client.create_conversation()
    if not session_id:
        bad("Could not create conversation session")
        return

    info(f"Created session #{session_id}")
    for i, q in enumerate(CHAT_TURNS, 1):
        info(f"Turn {i}: {q}")
        t0 = time.time()
        resp = client.chat(session_id, q)
        elapsed = time.time() - t0
        if resp and resp.get("answer"):
            preview   = resp["answer"][:220].replace("\n", " ")
            citations = resp.get("citations", [])
            ok(f"({elapsed:.1f}s, {len(citations)} citations) {preview}…")
        else:
            bad(f"No reply in {elapsed:.1f}s — resp={resp}")
        print()

    client.delete_conversation(session_id)
    info(f"Session #{session_id} deleted")


# ── Summary ───────────────────────────────────────────────────────────────────

def print_summary(results: list[CatResult]):
    header("SUMMARY — Categorization")

    intents = sorted({r.case.expected for r in results})
    for intent in intents:
        group   = [r for r in results if r.case.expected == intent]
        n_pass  = sum(1 for r in group if r.passed)
        colour  = G if n_pass == len(group) else (Y if n_pass > 0 else R)
        line    = f"  {colour}{intent:15s}{RESET}  {n_pass}/{len(group)}"
        failed  = [r for r in group if not r.passed]
        if failed:
            labels = ", ".join(
                f"{r.case.label}→{r.actual or 'timeout'}" for r in failed
            )
            line += f"  {Y}({labels}){RESET}"
        print(line)

    n_pass = sum(1 for r in results if r.passed)
    n_total = len(results)
    pct = n_pass / n_total * 100 if n_total else 0
    colour = G if pct >= 80 else (Y if pct >= 60 else R)
    print(f"\n  {B}Overall accuracy: {colour}{n_pass}/{n_total}  ({pct:.0f}%){RESET}")
    return pct


# ── Cleanup ───────────────────────────────────────────────────────────────────

def cleanup(client: KVClient, results: list[CatResult]):
    header("CLEANUP")
    ids = [r.note_id for r in results if r.note_id]
    for note_id in ids:
        client.delete_note(note_id)
    ok(f"Deleted {len(ids)} test notes")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print(f"\n{B}{'='*64}{RESET}")
    print(f"{B}  KnowledgeVault Live Smoke Test{RESET}")
    print(f"{B}{'='*64}{RESET}")
    print(f"  Target  : {BASE_URL}")
    print(f"  Account : {EMAIL}")
    print(f"  Notes   : {len(NOTE_CASES)}  |  Ask questions: {len(ASK_QUESTIONS)}  |  Chat turns: {len(CHAT_TURNS)}")

    client = KVClient()

    header("AUTH")
    if not client.login(EMAIL, PASSWORD):
        bad(f"Login failed for {EMAIL} — is the backend running?")
        sys.exit(1)
    ok(f"Logged in as {EMAIL}")

    cat_results = phase1_categorization(client)

    # Re-login before each phase so token expiry never causes failures
    client.login(EMAIL, PASSWORD)
    phase2_ask(client)

    client.login(EMAIL, PASSWORD)
    phase3_chat(client)
    pct = print_summary(cat_results)

    if DO_CLEANUP:
        cleanup(client, cat_results)
    else:
        warn("KV_CLEANUP=0 — test notes kept for manual inspection")

    print(f"\n{B}{'='*64}{RESET}\n")
    sys.exit(0 if pct >= 70 else 1)


if __name__ == "__main__":
    main()
