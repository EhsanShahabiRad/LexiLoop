from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class UserDetail(Base):
    __tablename__ = "user_details"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    username = Column(String(50), nullable=True)
    active_language_pair_id = Column(Integer, ForeignKey("language_pairs.id"), nullable=True)

    user = relationship("User", back_populates="detail")
