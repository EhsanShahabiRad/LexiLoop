from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional
from app.models.refresh_token import RefreshToken
from datetime import datetime
from app.repositories.interfaces.i_refresh_token_repository import IRefreshTokenRepository

class PGRefreshTokenRepository(IRefreshTokenRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_id: int, token_hash: str, expires_at: datetime, user_agent: Optional[str] = None) -> RefreshToken:
        refresh_token = RefreshToken(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
            user_agent=user_agent,
        )
        self.db.add(refresh_token)
        await self.db.commit()
        await self.db.refresh(refresh_token)
        return refresh_token

    async def get_by_token_hash(self, token_hash: str) -> Optional[RefreshToken]:
        result = await self.db.execute(select(RefreshToken).where(RefreshToken.token_hash == token_hash))
        return result.scalars().first()

    async def revoke(self, token_hash: str):
        token: Optional[RefreshToken] = await self.get_by_token_hash(token_hash)
        if token and token.is_valid:  # type: ignore[attr-defined]
            token.is_valid = False  # type: ignore[attr-defined]
            token.revoked_at = datetime.utcnow()  # type: ignore[attr-defined]
            await self.db.commit()
            await self.db.refresh(token)
        return token

    async def revoke_all_for_user(self, user_id: int):
        result = await self.db.execute(select(RefreshToken).where(RefreshToken.user_id == user_id, RefreshToken.is_valid == True))
        tokens = result.scalars().all()
        for token in tokens:
            token.is_valid = False  # type: ignore[attr-defined]
            token.revoked_at = datetime.utcnow()  # type: ignore[attr-defined]
        await self.db.commit()
        return tokens 

    async def get_all_valid_for_user(self, user_id: int):
        result = await self.db.execute(
            select(RefreshToken).where(
                RefreshToken.user_id == user_id,
                RefreshToken.is_valid == True
            )
        )
        return result.scalars().all() 