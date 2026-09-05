import hashlib
import secrets
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import UserRegister, UserLogin, TokenResponse
from app.services.email_service import EmailService


RESET_CODE_TTL_MINUTES = 30


def _hash_code(code: str) -> str:
    return hashlib.sha256(code.encode()).hexdigest()


class AuthService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def register(self, data: UserRegister) -> User:
        if self.repo.get_by_email(data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        if self.repo.get_by_username(data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken",
            )
        return self.repo.create(
            username=data.username,
            email=data.email,
            hashed_password=hash_password(data.password),
            is_verified=True,
        )

    def login(self, data: UserLogin) -> TokenResponse:
        user = self.repo.get_by_email(data.email)
        if not user or not verify_password(data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )
        token = create_access_token(data={"sub": str(user.id)})
        return TokenResponse(access_token=token, token_type="bearer")

    def request_password_reset(self, email: str) -> None:
        """Generate a 6-digit reset code, store its hash, email the code.
        Returns silently even if no account exists (avoid disclosing enumeration)."""
        user = self.repo.get_by_email(email)
        if not user:
            return
        code = f"{secrets.randbelow(1_000_000):06d}"
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=RESET_CODE_TTL_MINUTES)
        self.repo.set_reset_token(user, _hash_code(code), expires_at)
        EmailService.send_password_reset(user.email, user.username, code)

    def reset_password(self, email: str, code: str, new_password: str) -> None:
        user = self.repo.get_by_email(email)
        invalid = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset code.",
        )
        if not user or not user.reset_token_hash or not user.reset_token_expires_at:
            raise invalid
        expires_at = user.reset_token_expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        if expires_at < datetime.now(timezone.utc):
            raise invalid
        if not secrets.compare_digest(user.reset_token_hash, _hash_code(code)):
            raise invalid
        self.repo.update_password(user, hash_password(new_password))

    def update_username(self, user: User, username: str) -> User:
        username = username.strip()
        if not username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username cannot be empty",
            )
        existing = self.repo.get_by_username(username)
        if existing and existing.id != user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken",
            )
        return self.repo.update_username(user, username)
