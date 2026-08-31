"""SMTP email service — used only for password reset codes.

Works with any SMTP provider (Gmail app-password, Brevo, SendGrid, Mailgun...).
"""

import logging
import smtplib
from email.message import EmailMessage

from app.core.config import settings

logger = logging.getLogger(__name__)


class EmailService:
    @classmethod
    def _send(cls, to_email: str, subject: str, html: str, text: str) -> bool:
        if not settings.SMTP_HOST or not settings.SMTP_USER or not settings.SMTP_PASSWORD:
            logger.warning("SMTP not configured — skipping email to %s", to_email)
            return False
        msg = EmailMessage()
        msg["From"] = settings.EMAIL_FROM
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(text)
        msg.add_alternative(html, subtype="html")
        try:
            if settings.SMTP_USE_SSL:
                with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT, timeout=15) as s:
                    s.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                    s.send_message(msg)
            else:
                with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=15) as s:
                    s.ehlo()
                    if settings.SMTP_USE_TLS:
                        s.starttls()
                        s.ehlo()
                    s.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                    s.send_message(msg)
            logger.info("Email sent to %s: %s", to_email, subject)
            return True
        except Exception as exc:
            logger.error("Failed to send email to %s: %s", to_email, exc)
            return False

    @classmethod
    def send_password_reset(cls, to_email: str, username: str, code: str) -> bool:
        html = f"""
        <div style="font-family:sans-serif;max-width:480px;margin:0 auto;padding:32px">
          <h2 style="color:#4F46E5">Reset your KnowledgeVault password</h2>
          <p>Hi <strong>{username}</strong>,</p>
          <p>Use the code below to reset your password. It expires in 30 minutes.</p>
          <div style="font-size:32px;letter-spacing:6px;font-weight:700;
                      background:#F3F4F6;padding:16px;border-radius:12px;
                      text-align:center;margin:20px 0">{code}</div>
          <p style="color:#6b7280;font-size:13px">
            If you did not request a password reset, ignore this email — your password will not change.
          </p>
        </div>
        """
        text = (
            f"Hi {username},\n\nYour KnowledgeVault password reset code is: {code}\n\n"
            "It expires in 30 minutes. If you did not request this, ignore this email."
        )
        return cls._send(to_email, "Reset your KnowledgeVault password", html, text)
