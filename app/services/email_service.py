"""
Email service using Resend.
Sends transactional emails (verification, future notifications).
"""

import logging
import requests

from app.core.config import settings

logger = logging.getLogger(__name__)


class EmailService:
    _BASE = "https://api.resend.com"

    @classmethod
    def send_verification(cls, to_email: str, username: str, token: str) -> bool:
        """Send account verification email. Returns True on success."""
        if not settings.RESEND_API_KEY:
            logger.warning("RESEND_API_KEY not set — skipping verification email")
            return False

        verify_url = f"{settings.APP_BASE_URL}/auth/verify/{token}"

        html = f"""
        <div style="font-family:sans-serif;max-width:480px;margin:0 auto;padding:32px">
          <h2 style="color:#4F46E5">Verify your KnowledgeVault account</h2>
          <p>Hi <strong>{username}</strong>,</p>
          <p>Click the button below to verify your email address and activate your account.</p>
          <a href="{verify_url}"
             style="display:inline-block;margin:16px 0;padding:12px 24px;
                    background:#4F46E5;color:#fff;border-radius:8px;
                    text-decoration:none;font-weight:600">
            Verify Email
          </a>
          <p style="color:#6b7280;font-size:13px">
            Or copy this link: {verify_url}
          </p>
          <p style="color:#6b7280;font-size:13px">
            This link expires in 24 hours. If you did not create an account, you can ignore this email.
          </p>
        </div>
        """

        try:
            r = requests.post(
                f"{cls._BASE}/emails",
                headers={
                    "Authorization": f"Bearer {settings.RESEND_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "from": settings.EMAIL_FROM,
                    "to": [to_email],
                    "subject": "Verify your KnowledgeVault account",
                    "html": html,
                },
                timeout=10,
            )
            r.raise_for_status()
            logger.info("Verification email sent to %s", to_email)
            return True
        except Exception as exc:
            logger.error("Failed to send verification email to %s: %s", to_email, exc)
            return False
