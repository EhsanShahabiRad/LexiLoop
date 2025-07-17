from fastapi import Depends
from app.db.session import get_db
from app.repositories.implementations.pg_refresh_token_repository import PGRefreshTokenRepository

def get_refresh_token_repository(db=Depends(get_db)):
    return PGRefreshTokenRepository(db) 