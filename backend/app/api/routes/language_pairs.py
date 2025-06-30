from fastapi import APIRouter, Depends
from app.repositories.implementations.pg_language_pair_repository import PgLanguagePairRepository
from app.repositories.interfaces.i_language_pair_repository import ILanguagePairRepository
from app.schemas.language_pair_schema import LanguagePairRead
from app.mappers.language_pair_mapper import to_language_pair_read

router = APIRouter()

@router.get("/", response_model=list[LanguagePairRead])
async def get_language_pairs(repo: ILanguagePairRepository = Depends(PgLanguagePairRepository)):
    pairs = await repo.get_all()
    return [to_language_pair_read(p) for p in pairs]
