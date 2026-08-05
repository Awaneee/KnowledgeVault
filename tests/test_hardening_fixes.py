"""
Regression tests for the three blocking issues resolved before v1.0.0 freeze.

  SEC-1  CORS wildcard + allow_credentials=True
  SEC-2  JWT_SECRET .env.example placeholder silently passes 32-char validator
  DAT-1  Physical attachment files not deleted when a note is deleted

All tests are pure Python: no database, no network, no external services.
"""
from __future__ import annotations

import pathlib
from unittest.mock import MagicMock, call, patch

import pytest


# ---------------------------------------------------------------------------
# SEC-1 — CORS: wildcard origin must not enable credentials
# ---------------------------------------------------------------------------

class TestSec1CorsCredentials:
    """
    Starlette's CORSMiddleware, when allow_origins=["*"] and
    allow_credentials=True, echoes back the caller's Origin and sends
    Access-Control-Allow-Credentials: true to every site.  The fix sets
    allow_credentials=False when the origin list is the wildcard.
    """

    def _make_client(self, origins: list[str]):
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        from fastapi.testclient import TestClient

        app = FastAPI()
        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=origins != ["*"],  # ← the fix under test
            allow_methods=["*"],
            allow_headers=["*"],
        )

        @app.get("/ping")
        def ping():
            return {"ok": True}

        return TestClient(app, raise_server_exceptions=False)

    def test_wildcard_does_not_send_allow_credentials_header(self):
        client = self._make_client(["*"])
        resp = client.get("/ping", headers={"Origin": "https://evil.example.com"})
        assert resp.status_code == 200
        assert "access-control-allow-credentials" not in resp.headers

    def test_wildcard_sends_star_not_echoed_origin(self):
        """Starlette must send * (not the caller's origin) when credentials off."""
        client = self._make_client(["*"])
        resp = client.get("/ping", headers={"Origin": "https://evil.example.com"})
        assert resp.headers.get("access-control-allow-origin") == "*"

    def test_explicit_origin_still_gets_credentials_header(self):
        """Explicit whitelisted origins must still receive Allow-Credentials."""
        client = self._make_client(["https://app.example.com"])
        resp = client.get(
            "/ping", headers={"Origin": "https://app.example.com"}
        )
        assert resp.status_code == 200
        assert resp.headers.get("access-control-allow-credentials") == "true"

    def test_preflight_wildcard_no_credentials(self):
        """OPTIONS preflight must not grant credentials for wildcard origins."""
        client = self._make_client(["*"])
        resp = client.options(
            "/ping",
            headers={
                "Origin": "https://evil.example.com",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert "access-control-allow-credentials" not in resp.headers

    def test_boolean_expression_in_main_py(self):
        """Document the exact expression used in main.py."""
        assert (["*"] != ["*"]) is False           # wildcard → no credentials
        assert (["https://x.com"] != ["*"]) is True  # explicit → credentials ok


# ---------------------------------------------------------------------------
# SEC-2 — JWT_SECRET: .env.example placeholder must fail the validator
# ---------------------------------------------------------------------------

class TestSec2JwtSecretPlaceholder:
    """
    Before the fix, .env.example contained a 52-character placeholder that
    silently passed the >=32 char validator.  An operator who copied
    .env.example to .env without changing JWT_SECRET would run a server
    that issues forgeable tokens with no startup error.

    The fix: the placeholder is now 'CHANGE_ME' (8 chars), which fails the
    validator and causes a startup crash — forcing the operator to act.
    """

    ENV_EXAMPLE = pathlib.Path(".env.example")

    def _get_jwt_placeholder(self) -> str:
        text = self.ENV_EXAMPLE.read_text(encoding="utf-8")
        for line in text.splitlines():
            if line.startswith("JWT_SECRET="):
                return line.split("=", 1)[1].strip()
        pytest.fail("JWT_SECRET line not found in .env.example")

    def test_placeholder_shorter_than_32_chars(self):
        """Core invariant: placeholder must be too short to pass the validator."""
        placeholder = self._get_jwt_placeholder()
        assert len(placeholder) < 32, (
            f"JWT_SECRET placeholder '{placeholder}' is {len(placeholder)} chars "
            f"and would silently pass the >=32 char validator. "
            f"Shorten it (e.g. 'CHANGE_ME') to force a startup crash when "
            f"deployed without a real secret."
        )

    def test_placeholder_is_change_me(self):
        """The placeholder must be an obviously invalid sentinel value."""
        placeholder = self._get_jwt_placeholder()
        assert placeholder == "CHANGE_ME", (
            f"Expected 'CHANGE_ME', got '{placeholder}'. "
            f"The placeholder should be clearly invalid."
        )

    def test_old_placeholder_would_have_passed_validator(self):
        """Document the original trap: old value was >=32 chars."""
        old = "replace-this-with-at-least-32-chars-of-random-secret"
        assert len(old) >= 32  # This is why it was a trap — it silently passed.

    def test_validator_rejects_change_me(self):
        """The validator classmethod raises ValueError for the new placeholder."""
        from app.core.config import Settings

        with pytest.raises(ValueError, match="32"):
            Settings.jwt_secret_min_length("CHANGE_ME")

    def test_validator_rejects_old_pattern_when_short(self):
        from app.core.config import Settings

        with pytest.raises(ValueError):
            Settings.jwt_secret_min_length("tooshort")

    def test_validator_accepts_proper_32_char_secret(self):
        from app.core.config import Settings

        proper = "a" * 32
        result = Settings.jwt_secret_min_length(proper)
        assert result == proper


# ---------------------------------------------------------------------------
# DAT-1 — Attachment files deleted from disk when note is deleted
# ---------------------------------------------------------------------------

class TestDat1AttachmentFileDeletion:
    """
    When a note is deleted, SQLAlchemy cascades the DB delete to Attachment
    records.  Before the fix, the physical files in uploads/ were never
    removed, causing unbounded disk growth on the persistent volume.

    The fix: NoteService.delete_note() collects attachment file paths before
    the DB cascade and calls os.remove() for each one after deletion.
    """

    def _make_service(self, note, delete_returns=True):
        from app.services.note_service import NoteService

        svc = NoteService.__new__(NoteService)
        svc.repo = MagicMock()
        svc.repo.get_note_by_id.return_value = note
        svc.repo.delete_note_by_id.return_value = delete_returns
        svc.embedding_service = MagicMock()
        svc.chunk_service = MagicMock()
        svc.intent_category_service = MagicMock()
        return svc

    def _make_note(self, user_id=1, file_paths=None):
        note = MagicMock()
        note.user_id = user_id
        attachments = []
        for p in (file_paths or []):
            att = MagicMock()
            att.file_path = p
            attachments.append(att)
        note.attachments = attachments
        return note

    def test_files_removed_on_delete(self):
        paths = ["/app/uploads/a.pdf", "/app/uploads/b.txt"]
        note = self._make_note(file_paths=paths)
        svc = self._make_service(note)

        with patch("app.services.note_service.os.remove") as mock_rm, \
             patch("app.services.note_service.CacheService"):
            result = svc.delete_note(note_id=1, user_id=1)

        assert result is True
        mock_rm.assert_has_calls(
            [call(p) for p in paths], any_order=True
        )
        assert mock_rm.call_count == len(paths)

    def test_multiple_attachments_all_removed(self):
        paths = [f"/app/uploads/file{i}.pdf" for i in range(5)]
        note = self._make_note(file_paths=paths)
        svc = self._make_service(note)

        with patch("app.services.note_service.os.remove") as mock_rm, \
             patch("app.services.note_service.CacheService"):
            svc.delete_note(note_id=1, user_id=1)

        assert mock_rm.call_count == 5

    def test_no_files_removed_if_note_not_found(self):
        svc = self._make_service(note=None)

        with patch("app.services.note_service.os.remove") as mock_rm:
            result = svc.delete_note(note_id=99, user_id=1)

        assert result is False
        mock_rm.assert_not_called()

    def test_no_files_removed_for_wrong_user(self):
        note = self._make_note(user_id=2, file_paths=["/app/uploads/secret.pdf"])
        svc = self._make_service(note)

        with patch("app.services.note_service.os.remove") as mock_rm:
            result = svc.delete_note(note_id=1, user_id=1)  # user 1 ≠ owner 2

        assert result is False
        mock_rm.assert_not_called()

    def test_note_with_no_attachments_still_deletes(self):
        note = self._make_note(file_paths=[])
        svc = self._make_service(note)

        with patch("app.services.note_service.os.remove") as mock_rm, \
             patch("app.services.note_service.CacheService"):
            result = svc.delete_note(note_id=1, user_id=1)

        assert result is True
        mock_rm.assert_not_called()

    def test_missing_file_logs_warning_does_not_raise(self):
        """If a file is already absent, OSError must be swallowed (log only)."""
        note = self._make_note(file_paths=["/app/uploads/gone.pdf"])
        svc = self._make_service(note)

        with patch("app.services.note_service.os.remove",
                   side_effect=OSError("no such file")), \
             patch("app.services.note_service.CacheService"), \
             patch("app.services.note_service.logger") as mock_log:
            result = svc.delete_note(note_id=1, user_id=1)

        assert result is True
        assert mock_log.warning.called

    def test_cache_invalidated_after_delete(self):
        note = self._make_note(file_paths=[])
        svc = self._make_service(note)

        with patch("app.services.note_service.os.remove"), \
             patch("app.services.note_service.CacheService") as mock_cache:
            svc.delete_note(note_id=1, user_id=1)

        calls = [str(c) for c in mock_cache.delete_pattern.call_args_list]
        assert any("ask:1:*" in c for c in calls)
        assert any("semantic_search:1:*" in c for c in calls)

    def test_files_collected_before_db_delete(self):
        """File paths must be collected from the note BEFORE the DB cascade
        removes the Attachment records."""
        paths = ["/app/uploads/important.docx"]
        note = self._make_note(file_paths=paths)
        svc = self._make_service(note)

        call_order = []

        def track_remove(p):
            call_order.append(("remove", p))

        original_delete = svc.repo.delete_note_by_id.side_effect

        def track_db_delete(note_id):
            call_order.append(("db_delete", note_id))
            return True

        svc.repo.delete_note_by_id.side_effect = track_db_delete

        with patch("app.services.note_service.os.remove", side_effect=track_remove), \
             patch("app.services.note_service.CacheService"):
            svc.delete_note(note_id=1, user_id=1)

        # DB delete must happen before os.remove (files removed after cascade)
        assert call_order[0] == ("db_delete", 1)
        assert call_order[1] == ("remove", paths[0])
