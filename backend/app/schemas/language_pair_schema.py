from pydantic import BaseModel

class LanguagePairRead(BaseModel):
    id: int
    source_language_name: str
    target_language_name: str

    class Config:
        from_attributes = True
