from abc import ABC, abstractmethod
from typing import List, Optional
from app.models.language_pair import LanguagePair

class ILanguagePairRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[LanguagePair]:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[LanguagePair]:
        pass

    @abstractmethod
    async def get_by_langs(self, source_lang_id: int, target_lang_id: int) -> Optional[LanguagePair]:
        pass
