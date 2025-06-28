from typing import Optional
from pydantic import BaseModel


class UserDetailBase(BaseModel):
    name: Optional[str] = None
    active_language_pair_id: Optional[int] = None


class UserDetailCreate(UserDetailBase):
    pass


class UserDetailUpdate(UserDetailBase):
    pass


class UserDetailRead(UserDetailBase):
    user_id: int

    class Config:
        from_attributes = True
