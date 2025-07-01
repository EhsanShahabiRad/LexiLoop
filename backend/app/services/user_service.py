from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.jwt import create_access_token
from app.models.user import User
from app.schemas.user_profile_schema import UserProfileUpdate
from app.schemas.user_detail_schema import UserDetailUpdate
from app.repositories.interfaces.i_user_repository import IUserRepository
from app.repositories.interfaces.i_user_detail_repository import IUserDetailRepository
from app.repositories.interfaces.i_language_pair_repository import ILanguagePairRepository


class UserService:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def update_profile(
        self,
        db: AsyncSession,
        current_user: User,
        update: UserProfileUpdate,
        user_detail_repo: IUserDetailRepository,
        language_pair_repo: ILanguagePairRepository
    ) -> str:
        if current_user.updated_at and datetime.utcnow() - current_user.updated_at < timedelta(seconds=10):
            raise HTTPException(status_code=429, detail="Too many updates. Please wait before trying again.")

        if update.email and current_user.email and update.email != current_user.email:
            raise HTTPException(status_code=400, detail="Email cannot be changed.")

        existing = await self.user_repository.get_by_username(update.username)
        if existing and existing.id != current_user.id:
            raise HTTPException(status_code=400, detail="Username is already taken.")

        source_lang_id = target_lang_id = None
        if update.active_language_pair_id is not None:
            pair = await language_pair_repo.get_by_id(update.active_language_pair_id)
            if not pair:
                raise HTTPException(status_code=400, detail="Invalid language pair.")
            source_lang_id = pair.source_lang_id
            target_lang_id = pair.target_lang_id

        current_user.username = update.username
        if update.email and not current_user.email:
            current_user.email = update.email
        current_user.updated_at = datetime.utcnow()
        await self.user_repository.update(current_user)

        name = update.name if update.name not in (None, "") else None

        user_detail = await user_detail_repo.get_user_detail_by_user_id(current_user.id)
        if user_detail:
            detail_update = UserDetailUpdate(
                name=name,
                source_language_id=source_lang_id,
                target_language_id=target_lang_id,
            )
            await user_detail_repo.update_user_detail(current_user.id, detail_update)
        else:
            await user_detail_repo.create_user_detail(
                user_id=current_user.id,
                name=name,
                source_language_id=source_lang_id,
                target_language_id=target_lang_id,
            )

        
        return create_access_token(
            user_id=current_user.id,
            source_lang_id=source_lang_id,
            target_lang_id=target_lang_id,
            name=name,
)

    async def get_user_by_id(self, user_id: int) -> User:
        return await self.user_repository.get_by_id(user_id)
