from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Meaning(Base):
    __tablename__ = "meanings"

    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey("words.id"), nullable=False)
    pos_id = Column(Integer, ForeignKey("pos.id"), nullable=False)
    meaning_text = Column(Text, nullable=False)

    word = relationship("Word", back_populates="meanings")
    pos = relationship("POS", back_populates="meanings")
    user_words = relationship("UserWord", back_populates="meaning")
