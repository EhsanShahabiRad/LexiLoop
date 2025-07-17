from fastapi import Depends
from app.dependencies.refresh_token_repository import get_refresh_token_repository
from app.repositories.interfaces.i_refresh_token_repository import IRefreshTokenRepository
from app.services.refresh_token_service import RefreshTokenService

def get_refresh_token_service(
    repo: IRefreshTokenRepository = Depends(get_refresh_token_repository)
) -> RefreshTokenService:
    return RefreshTokenService(repo) 