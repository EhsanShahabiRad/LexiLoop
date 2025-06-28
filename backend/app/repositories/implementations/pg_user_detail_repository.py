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


class PgUserDetailRepository(IUserDetailRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user_detail(self, user_id: int, data: UserDetailCreate) -> UserDetailRead:
        user_detail = UserDetail(
            user_id=user_id,
            name=data.name,
            active_language_pair_id=data.active_language_pair_id,
        )
        self.session.add(user_detail)
        await self.session.commit()
        await self.session.refresh(user_detail)
        return UserDetailRead.from_orm(user_detail)

    async def get_user_detail_by_user_id(self, user_id: int) -> Optional[UserDetailRead]:
        result = await self.session.execute(
            select(UserDetail).where(UserDetail.user_id == user_id)
        )
        user_detail = result.scalars().first()
        if user_detail:
            return UserDetailRead.from_orm(user_detail)
        return None

    async def update_user_detail(self, user_id: int, data: UserDetailUpdate) -> Optional[UserDetailRead]:
        result = await self.session.execute(
            select(UserDetail).where(UserDetail.user_id == user_id)
        )
        user_detail = result.scalars().first()
        if not user_detail:
            return None

        if data.name is not None:
            user_detail.name = data.name
        if data.active_language_pair_id is not None:
            user_detail.active_language_pair_id = data.active_language_pair_id

        await self.session.commit()
        await self.session.refresh(user_detail)
        return UserDetailRead.from_orm(user_detail)
