from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(100), nullable=False)
    language_pair_id = Column(Integer, ForeignKey("language_pairs.id"), nullable=False)

    language_pair = relationship("LanguagePair", backref="words")
    meanings = relationship("Meaning", back_populates="word")
