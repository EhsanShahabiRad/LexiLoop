from typing import Optional
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserUpdate, UserRead
from app.repositories.interfaces.i_user_repository import IUserRepository
from app.mappers.user_mapper import UserMapper


class UserService:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def get_user_by_id(self, user_id: int) -> Optional[UserRead]:
        user = await self.user_repository.get_by_id(user_id)
        return UserMapper.to_read(user) if user else None

    async def get_user_by_email(self, email: str) -> Optional[UserRead]:
        user = await self.user_repository.get_by_email(email)
        return UserMapper.to_read(user) if user else None

    async def get_user_by_username(self, username: str) -> Optional[UserRead]:
        user = await self.user_repository.get_by_username(username)
        return UserMapper.to_read(user) if user else None

    async def register_user(self, user_in: UserCreate) -> UserRead:
        hashed_password = None
        if user_in.auth_provider == "local" and user_in.password:
            hashed_password = UserMapper.hash_password(user_in.password)

        user = UserMapper.to_model(user_in, hashed_password)
        created = await self.user_repository.create(user)
        return UserMapper.to_read(created)

    async def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[UserRead]:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            return None
        updated_model = UserMapper.update_model(user, user_update)
        updated = await self.user_repository.update(updated_model)
        return UserMapper.to_read(updated)
