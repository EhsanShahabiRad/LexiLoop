from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.user_detail import UserDetail
from app.repositories.interfaces.i_user_detail_repository import IUserDetailRepository
from app.schemas.user_detail_schema import (
    UserDetailCreate,
    UserDetailUpdate,
    UserDetailRead,
)
from app.mappers.user_detail_mapper import UserDetailMapper


class PgUserDetailRepository(IUserDetailRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user_detail(self, user_id: int, data: UserDetailCreate) -> UserDetailRead:
        user_detail = UserDetailMapper.from_create(user_id, data)
        self.session.add(user_detail)
        await self.session.commit()
        await self.session.refresh(user_detail)
        return UserDetailMapper.to_read(user_detail)

    async def get_user_detail_by_user_id(self, user_id: int) -> Optional[UserDetailRead]:
        result = await self.session.execute(
            select(UserDetail).where(UserDetail.user_id == user_id)
        )
        user_detail = result.scalars().first()
        if user_detail:
            return UserDetailMapper.to_read(user_detail)
        return None

    async def update_user_detail(self, user_id: int, data: UserDetailUpdate) -> Optional[UserDetailRead]:
        result = await self.session.execute(
            select(UserDetail).where(UserDetail.user_id == user_id)
        )
        user_detail = result.scalars().first()
        if not user_detail:
            return None

        updated = UserDetailMapper.update_model(user_detail, data)
        await self.session.commit()
        await self.session.refresh(updated)
        return UserDetailMapper.to_read(updated)
