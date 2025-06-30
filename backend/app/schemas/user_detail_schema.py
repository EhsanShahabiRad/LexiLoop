from typing import Optional
from pydantic import BaseModel


class UserDetailBase(BaseModel):
    name: Optional[str] = None
    active_language_pair_id: Optional[int] = None


class UserDetailCreate(UserDetailBase):
    pass


class UserDetailUpdate(BaseModel):
    name: Optional[str] = None
    source_language_id: Optional[int] = None
    target_language_id: Optional[int] = None


from pydantic import BaseModel
from typing import Optional

class UserDetailRead(BaseModel):
    id: int
    user_id: int
    name: Optional[str] = None
    source_language_id: Optional[int] = None 
    target_language_id: Optional[int] = None 

    model_config = {
        "from_attributes": True
    }

