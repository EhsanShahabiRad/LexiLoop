import hashlib
from datetime import datetime, timedelta
from typing import Optional
from app.repositories.interfaces.i_refresh_token_repository import IRefreshTokenRepository
from app.models.refresh_token import RefreshToken

class RefreshTokenService:
    def __init__(self, repo: IRefreshTokenRepository):
        self.repo = repo

    def hash_token(self, token: str) -> str:
        return hashlib.sha256(token.encode()).hexdigest()

    async def enforce_max_sessions(self, user_id: int, max_sessions: int = 2):
        tokens = await self.repo.get_all_valid_for_user(user_id)
        if len(tokens) > max_sessions:
            # Sort by created_at (oldest first)
            tokens_to_revoke = sorted(tokens, key=lambda t: t.created_at)[:-max_sessions]
            for token in tokens_to_revoke:
                await self.repo.revoke(token.token_hash)

    async def create_token(self, user_id: int, token: str, expires_in_days: int, user_agent: Optional[str] = None) -> RefreshToken:
        token_hash = self.hash_token(token)
        expires_at = datetime.utcnow() + timedelta(days=expires_in_days)
        new_token = await self.repo.create(user_id, token_hash, expires_at, user_agent)
        await self.enforce_max_sessions(user_id, max_sessions=2)
        return new_token

    async def validate_token(self, token: str) -> Optional[RefreshToken]:
        token_hash = self.hash_token(token)
        db_token = await self.repo.get_by_token_hash(token_hash)
        if db_token and db_token.is_valid and db_token.expires_at > datetime.utcnow():
            return db_token
        return None

    async def revoke_token(self, token: str):
        token_hash = self.hash_token(token)
        return await self.repo.revoke(token_hash)

    async def rotate_token(self, user_id: int, old_token: str, new_token: str, expires_in_days: int, user_agent: Optional[str] = None):
        # Revoke old token
        await self.revoke_token(old_token)
        # Create new token
        new_token = await self.create_token(user_id, new_token, expires_in_days, user_agent)
        await self.enforce_max_sessions(user_id, max_sessions=2)
        return new_token

    async def revoke_all_for_user(self, user_id: int):
        return await self.repo.revoke_all_for_user(user_id) 