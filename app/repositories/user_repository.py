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

    def get_by_verification_token(self, token: str) -> User | None:
        return self.db.query(User).filter(User.verification_token == token).first()

    def create(
        self,
        username: str,
        email: str,
        hashed_password: str,
        verification_token: str | None = None,
        is_verified: bool = False,
    ) -> User:
        user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            verification_token=verification_token,
            is_verified=is_verified,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def mark_verified(self, user: User) -> None:
        user.is_verified = True
        user.verification_token = None
        self.db.commit()
