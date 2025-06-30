from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.implementations.pg_language_pair_repository import PgLanguagePairRepository
from app.repositories.interfaces.i_language_pair_repository import ILanguagePairRepository

def get_language_pair_repository(
    db: AsyncSession = Depends(get_db),
) -> ILanguagePairRepository:
    return PgLanguagePairRepository(db)
