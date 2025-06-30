from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import Depends
from app.models.language_pair import LanguagePair
from app.db.session import get_db
from app.repositories.interfaces.i_language_pair_repository import ILanguagePairRepository

class PgLanguagePairRepository(ILanguagePairRepository):
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get_all(self) -> list[LanguagePair]:
        result = await self.db.execute(
            select(LanguagePair).options(
                joinedload(LanguagePair.source_lang),
                joinedload(LanguagePair.target_lang)
            )
        )
        return result.scalars().all()

    async def get_by_id(self, id: int) -> LanguagePair | None:
        result = await self.db.execute(
            select(LanguagePair)
            .options(
                joinedload(LanguagePair.source_lang),
                joinedload(LanguagePair.target_lang),
            )
            .where(LanguagePair.id == id)
        )
        return result.scalars().first()
    
    async def get_by_langs(self, source_lang_id: int, target_lang_id: int) -> LanguagePair | None:
         result = await self.db.execute(
            select(LanguagePair)
            .where(LanguagePair.source_lang_id == source_lang_id)
            .where(LanguagePair.target_lang_id == target_lang_id)
         )
         return result.scalars().first()
