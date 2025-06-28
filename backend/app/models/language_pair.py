from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class LanguagePair(Base):
    __tablename__ = "language_pairs"
    __table_args__ = (UniqueConstraint("source_lang_id", "target_lang_id"),)

    id = Column(Integer, primary_key=True, index=True)
    source_lang_id = Column(Integer, ForeignKey("languages.id", ondelete="CASCADE"), nullable=False)
    target_lang_id = Column(Integer, ForeignKey("languages.id", ondelete="CASCADE"), nullable=False)

    source_lang = relationship("Language", foreign_keys=[source_lang_id])
    target_lang = relationship("Language", foreign_keys=[target_lang_id])
