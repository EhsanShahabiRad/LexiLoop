from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserProfileRead(BaseModel):
    id: int
    email: EmailStr
    username: Optional[str] = None
    name: Optional[str] = None
    active_language_pair_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class UserProfileUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    name: Optional[str] = None
    active_language_pair_id: Optional[int] = None
