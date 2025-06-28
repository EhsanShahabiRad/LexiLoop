from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class UserDetail(Base):
    __tablename__ = "user_details"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    name = Column(String(100), nullable=True)

    source_language_id = Column(Integer, ForeignKey("languages.id", ondelete="SET NULL"))
    target_language_id = Column(Integer, ForeignKey("languages.id", ondelete="SET NULL"))

    user = relationship("User", back_populates="detail")
    source_language = relationship("Language", foreign_keys=[source_language_id])
    target_language = relationship("Language", foreign_keys=[target_language_id])
