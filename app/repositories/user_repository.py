from datetime import datetime

from sqlalchemy.orm import Session
from app.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()

    def create(
        self,
        username: str,
        email: str,
        hashed_password: str,
        is_verified: bool = True,
    ) -> User:
        user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            is_verified=is_verified,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def set_reset_token(self, user: User, token_hash: str, expires_at: datetime) -> None:
        user.reset_token_hash = token_hash
        user.reset_token_expires_at = expires_at
        self.db.commit()

    def update_password(self, user: User, hashed_password: str) -> None:
        user.hashed_password = hashed_password
        user.reset_token_hash = None
        user.reset_token_expires_at = None
        self.db.commit()
