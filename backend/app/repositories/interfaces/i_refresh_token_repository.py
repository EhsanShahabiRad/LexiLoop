from abc import ABC, abstractmethod
from typing import Optional
from datetime import datetime
from app.models.refresh_token import RefreshToken

class IRefreshTokenRepository(ABC):
    @abstractmethod
    async def create(self, user_id: int, token_hash: str, expires_at: datetime, user_agent: Optional[str] = None) -> RefreshToken:
        pass

    @abstractmethod
    async def get_by_token_hash(self, token_hash: str) -> Optional[RefreshToken]:
        pass

    @abstractmethod
    async def revoke(self, token_hash: str):
        pass

    @abstractmethod
    async def revoke_all_for_user(self, user_id: int):
        pass 