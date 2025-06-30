from app.models.language_pair import LanguagePair
from app.schemas.language_pair_schema import LanguagePairRead

def to_language_pair_read(pair: LanguagePair) -> LanguagePairRead:
    return LanguagePairRead(
        id=pair.id,
        source_language_name=pair.source_lang.name,
        target_language_name=pair.target_lang.name,
    )
