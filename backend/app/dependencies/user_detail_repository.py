from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.implementations.pg_user_detail_repository import PGUserDetailRepository
from app.repositories.interfaces.i_user_detail_repository import IUserDetailRepository

def get_user_detail_repository(
    db: AsyncSession = Depends(get_db),
) -> IUserDetailRepository:
    return PGUserDetailRepository(db)
