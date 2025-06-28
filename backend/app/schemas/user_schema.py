from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    password: str  # plain password for registration


class UserRead(UserBase):
    id: int
    role: str
    is_email_verified: bool
    auth_provider: str
    provider_user_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None  # optional plain password update
    is_email_verified: Optional[bool] = None
    role: Optional[str] = None


class UserInDBBase(UserRead):
    password_hash: Optional[str] = None
