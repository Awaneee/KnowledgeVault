from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    has_avatar: bool = False

    model_config = {"from_attributes": True}

    @classmethod
    def from_user(cls, user) -> "UserResponse":
        return cls(
            id=user.id,
            username=user.username,
            email=user.email,
            has_avatar=bool(user.avatar_path),
        )


class UsernameUpdateRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class PasswordResetRequest(BaseModel):
    email: EmailStr
    code: str = Field(..., min_length=6, max_length=6)
    new_password: str = Field(..., min_length=8, max_length=128)
