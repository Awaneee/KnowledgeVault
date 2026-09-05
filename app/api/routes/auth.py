import os
import uuid

from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.limiter import limiter
from app.database.session import get_db
from app.schemas.auth import (
    UserRegister,
    UserLogin,
    UserResponse,
    UsernameUpdateRequest,
    TokenResponse,
    ForgotPasswordRequest,
    PasswordResetRequest,
)
from app.services.auth_service import AuthService
from app.api.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])

AVATAR_DIR = "uploads/avatars"
os.makedirs(AVATAR_DIR, exist_ok=True)

ALLOWED_AVATAR_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}


@router.post("/register", response_model=UserResponse, status_code=201)
@limiter.limit("5/minute")
def register(request: Request, data: UserRegister, db: Session = Depends(get_db)):
    user = AuthService(db).register(data)
    return UserResponse.from_user(user)


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
    return UserResponse.from_user(current_user)


@router.patch("/me", response_model=UserResponse)
def update_me(
    data: UsernameUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user = AuthService(db).update_username(current_user, data.username)
    return UserResponse.from_user(user)


@router.post("/me/avatar", response_model=UserResponse)
def upload_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in ALLOWED_AVATAR_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported image type '{ext}'. Allowed: "
            f"{', '.join(sorted(ALLOWED_AVATAR_EXTENSIONS))}",
        )

    content = file.file.read()
    if len(content) > settings.MAX_AVATAR_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"Image too large. Maximum allowed size is "
            f"{settings.MAX_AVATAR_BYTES // (1024 * 1024)} MB.",
        )

    old_path = current_user.avatar_path
    new_path = os.path.join(AVATAR_DIR, f"{uuid.uuid4()}{ext}")
    with open(new_path, "wb") as f:
        f.write(content)

    user = AuthService(db).repo.update_avatar_path(current_user, new_path)

    # Clean up the previous file now that the new one is committed.
    if old_path and old_path != new_path:
        try:
            os.remove(old_path)
        except OSError:
            pass

    return UserResponse.from_user(user)


@router.delete("/me/avatar", response_model=UserResponse)
def delete_avatar(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    old_path = current_user.avatar_path
    user = AuthService(db).repo.update_avatar_path(current_user, None)
    if old_path:
        try:
            os.remove(old_path)
        except OSError:
            pass
    return UserResponse.from_user(user)


@router.get("/me/avatar")
def get_avatar(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not current_user.avatar_path or not os.path.exists(current_user.avatar_path):
        raise HTTPException(status_code=404, detail="No profile picture set")
    return FileResponse(current_user.avatar_path)
