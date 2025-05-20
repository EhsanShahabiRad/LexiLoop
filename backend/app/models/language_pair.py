from sqlalchemy import Column, Integer, String
from app.db.base_class import Base
from sqlalchemy.orm import relationship

class LanguagePair(Base):
    __tablename__ = "language_pairs"

    id = Column(Integer, primary_key=True, index=True)
    source_lang = Column(String(10), nullable=False)
    target_lang = Column(String(10), nullable=False)

    
