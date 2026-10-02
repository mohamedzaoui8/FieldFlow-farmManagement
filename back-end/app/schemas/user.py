import re

from pydantic import BaseModel, EmailStr, field_validator


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("كلمة المرور يجب أن تكون على الأقل 8 أحرف")
        if not re.search(r"[A-zA-z\u0600-\u06ff]", v):
            raise ValueError("كلمة المرور يجب أن تحتوي على حرف كبير واحد على الأقل")


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None


class UserCreateResponse(BaseModel):
    message: str
    user: UserResponse
