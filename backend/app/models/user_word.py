from sqlalchemy import Column, Integer, ForeignKey, Boolean, Float, DateTime, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class UserWord(Base):
    __tablename__ = "user_words"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    meaning_id = Column(Integer, ForeignKey("meanings.id"), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)

    ef_factor = Column(Float, default=2.5)
    interval_days = Column(Integer, default=1)
    next_review_date = Column(Date, nullable=True)

    added_at = Column(DateTime, default=datetime.utcnow)
    reviewed_at = Column(DateTime, nullable=True)
    review_count = Column(Integer, default=0)
    is_learned = Column(Boolean, default=False)

    user = relationship("User", backref="user_words")
    meaning = relationship("Meaning", back_populates="user_words")
    group = relationship("Group", back_populates="user_words")
