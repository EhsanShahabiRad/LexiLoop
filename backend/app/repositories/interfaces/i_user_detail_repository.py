from abc import ABC, abstractmethod
from typing import Optional
from app.schemas.user_detail_schema import (
    UserDetailCreate,
    UserDetailUpdate,
    UserDetailRead,
)


class IUserDetailRepository(ABC):
    @abstractmethod
    async def create_user_detail(self, user_id: int, data: UserDetailCreate) -> UserDetailRead:
        pass

    @abstractmethod
    async def get_user_detail_by_user_id(self, user_id: int) -> Optional[UserDetailRead]:
        pass

    @abstractmethod
    async def update_user_detail(self, user_id: int, data: UserDetailUpdate) -> Optional[UserDetailRead]:
        pass
