# KnowledgeVault Backend — v1.0.0 Release Candidate Audit

**Date:** 2026-08-05  
**Auditor:** Claude Sonnet 4.6 (automated)  
**Branch:** `main`  
**Freeze target:** 2026-08-07  
**Scope:** Production-blocking issues only. Feature gaps and performance ideas are excluded.

---

## Status

| ID | Severity | Finding | Status |
|----|----------|---------|--------|
| SEC-1 | HIGH | CORS wildcard + `allow_credentials=True` | ✅ RESOLVED |
| SEC-2 | HIGH | JWT_SECRET placeholder silently passes validator | ✅ RESOLVED |
| DAT-1 | HIGH | Physical attachment files never deleted from disk | ✅ RESOLVED |
| SEC-3 | MEDIUM | No `DELETE /attachments/{id}` endpoint | Open (post-freeze) |
| DAT-2 | MEDIUM | `sleep 15` in migrate service is fragile | Open (post-freeze) |
| DEP-1 | MEDIUM | `api` container has no healthcheck in docker-compose | Open (post-freeze) |
| DEP-2 | MEDIUM | `pytest` absent from `requirements.txt` | Open (post-freeze) |
| API-1 | LOW | New notes do not bust ask cache (by design) | Accepted |
| API-2 | LOW | `POST /notes/bulk` returns 200 on partial failure | Accepted |

---

## Resolved Blocking Issues

### SEC-1 — CORS wildcard + `allow_credentials=True` ✅ RESOLVED

**Fix applied:** `main.py`

```python
# Before
allow_credentials=True,

# After
allow_credentials=settings.CORS_ALLOWED_ORIGINS != ["*"],
```

When `CORS_ALLOWED_ORIGINS=["*"]` (the default), `allow_credentials` is now `False`. Starlette sends `Access-Control-Allow-Origin: *` without the credentials header. Explicit origin lists (production deployments) still get `allow_credentials=True`.

**Verified by:** `tests/test_hardening_fixes.py::TestSec1CorsCredentials` (5 tests, all passing)

---

### SEC-2 — JWT_SECRET placeholder silently passes validator ✅ RESOLVED

**Fix applied:** `.env.example`

```
# Before (52 chars — passed the >=32 validator silently)
JWT_SECRET=replace-this-with-at-least-32-chars-of-random-secret

# After (8 chars — fails the validator, forces startup crash)
JWT_SECRET=CHANGE_ME
```

An operator who copies `.env.example` to `.env` without changing `JWT_SECRET` now gets a `ValidationError` at startup with a message instructing them to generate a proper secret. The server does not start.

**Verified by:** `tests/test_hardening_fixes.py::TestSec2JwtSecretPlaceholder` (6 tests, all passing)

---

### DAT-1 — Physical attachment files never deleted from disk ✅ RESOLVED

**Fix applied:** `app/services/note_service.py`

```python
# Before
deleted = self.repo.delete_note_by_id(note_id)
if deleted:
    CacheService.delete_pattern(...)

# After
attachment_paths = [a.file_path for a in note.attachments]
deleted = self.repo.delete_note_by_id(note_id)
if deleted:
    for path in attachment_paths:
        try:
            os.remove(path)
        except OSError as exc:
            logger.warning("Could not remove attachment file %s: %s", path, exc)
    CacheService.delete_pattern(...)
```

File paths are collected from the ORM before the DB cascade removes Attachment records. Files are removed after the DB delete succeeds. A missing file (already gone from disk) logs a warning and does not fail the deletion.

**Verified by:** `tests/test_hardening_fixes.py::TestDat1AttachmentFileDeletion` (8 tests, all passing)

---

## Open Issues (Post-Freeze)

### SEC-3 — No `DELETE /attachments/{id}` endpoint (MEDIUM)

Attachments can be uploaded but not individually deleted by a user. Users cannot remove private files uploaded in error. Post-freeze scope.

---

### DAT-2 — `migrate` service uses hardcoded `sleep 15` (MEDIUM)

`docker-compose.yml` migrate service sleeps 15 seconds before running `alembic upgrade head` despite `depends_on: condition: service_healthy`. The sleep is redundant and unreliable on slow hardware. Post-freeze scope.

---

### DEP-1 — `api` container has no `healthcheck` in docker-compose (MEDIUM)

`GET /health` was implemented and works, but is not wired as a docker-compose `healthcheck` for the `api` service. Post-freeze scope.

```yaml
# Add to api service in docker-compose.yml:
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 60s
```

---

### DEP-2 — `pytest` absent from `requirements.txt` (MEDIUM)

The 20-file test suite exists but `pytest` is not listed as a dependency. CI pipelines cannot run tests from a clean image build without an additional install step. Post-freeze scope.

---

## Confirmed Non-Issues

| Item | Finding |
|------|---------|
| `datetime.utcnow()` in `security.py` | DeprecationWarning on Python 3.12+; base image is `python:3.11-slim`. Functions correctly. Not a blocker. |
| Redis bare `except Exception` in health check | Intentional — health check must not raise. Correct pattern. |
| Job queue `ack_job()` JSON string matching | `json.dumps` is deterministic for integer-keyed dicts in Python 3.7+. Not a bug. |
| SQLAlchemy cascade on note delete | Verified `cascade="all, delete-orphan"` on all five Note relationships. |
| Rate limiter | `slowapi` correctly wired. 429 handler registered. Routes correctly decorated. |
| SQL injection | All queries use SQLAlchemy ORM or parameterized `text()`. |
| Password hashing | bcrypt via passlib with `truncate_error=False`. Correct. |
| Docker non-root user | `appuser` UID 1001, `chown -R appuser /app /home/appuser`. Correct. |

---

## Test Suite Results

```
884 passed, 1 warning in 65.98s
```

The single warning is a `StarletteDeprecationWarning` about `httpx` vs `httpx2` in the `TestClient` import — not a test failure and not related to any fix.

---

## RECOMMENDATION

### ✅ READY TO FREEZE

All three blocking issues (SEC-1, SEC-2, DAT-1) have been resolved, tested, and verified. The full test suite passes with 884/884 tests. The remaining open items (SEC-3, DAT-2, DEP-1, DEP-2) are medium-severity operational improvements that do not prevent a v1.0.0 production release and are appropriate for the post-freeze backlog.
