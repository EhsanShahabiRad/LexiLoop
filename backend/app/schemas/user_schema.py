from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# ----- UserDetail -----

class UserDetailBase(BaseModel):
    username: Optional[str] = None
    active_language_pair_id: Optional[int] = None

class UserDetailCreate(UserDetailBase):
    pass

class UserDetailRead(UserDetailBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True


# ----- User -----

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    pass  # no password or username for now

class UserRead(UserBase):
    id: int
    is_email_verified: bool
    role: str
    created_at: datetime
    detail: Optional[UserDetailRead] = None  

    class Config:
        from_attributes = True
