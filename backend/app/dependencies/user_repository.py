from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.implementations.pg_user_repository import PGUserRepository
from app.repositories.interfaces.i_user_repository import IUserRepository

def get_user_repository(db: AsyncSession = Depends(get_db)) -> IUserRepository:
    return PGUserRepository(db)
