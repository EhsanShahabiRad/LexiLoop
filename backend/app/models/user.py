from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP, func
from app.db.base_class import Base
from sqlalchemy.orm import relationship
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    username = Column(String(50), unique=True)
    password_hash = Column(String(255), nullable=False)
    is_email_verified = Column(Boolean, default=False)
    active_language_pair_id = Column(Integer, ForeignKey("languagepair.id"))
    role = Column(String(20))
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
    active_language_pair_id = Column(Integer, ForeignKey("language_pairs.id"))
