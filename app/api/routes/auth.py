from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.core.limiter import limiter
from app.database.session import get_db
from app.schemas.auth import (
    UserRegister,
    UserLogin,
    UserResponse,
    TokenResponse,
    ForgotPasswordRequest,
    PasswordResetRequest,
)
from app.services.auth_service import AuthService
from app.api.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=201)
@limiter.limit("5/minute")
def register(request: Request, data: UserRegister, db: Session = Depends(get_db)):
    return AuthService(db).register(data)


@router.post("/login", response_model=TokenResponse)
@limiter.limit("10/minute")
def login(request: Request, data: UserLogin, db: Session = Depends(get_db)):
    return AuthService(db).login(data)


@router.post("/forgot-password")
@limiter.limit("3/minute")
def forgot_password(
    request: Request,
    data: ForgotPasswordRequest,
    db: Session = Depends(get_db),
):
    AuthService(db).request_password_reset(data.email)
    return {"message": "If an account exists for that email, a reset code has been sent."}


@router.post("/reset-password")
@limiter.limit("5/minute")
def reset_password(
    request: Request,
    data: PasswordResetRequest,
    db: Session = Depends(get_db),
):
    AuthService(db).reset_password(data.email, data.code, data.new_password)
    return {"message": "Password reset successful. You can now log in."}


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
