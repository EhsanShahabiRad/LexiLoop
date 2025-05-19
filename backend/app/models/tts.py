from sqlalchemy import Column, Integer, ForeignKey, String, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class TTS(Base):
    __tablename__ = "tts"

    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey("words.id"), nullable=False)
    language_pair_id = Column(Integer, ForeignKey("language_pairs.id"), nullable=False)

    audio_url = Column(Text, nullable=False)
    provider = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    word = relationship("Word", backref="tts_entries")
    language_pair = relationship("LanguagePair", backref="tts_entries")
