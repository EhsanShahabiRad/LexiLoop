from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=True)
    auth_provider = Column(String(50), nullable=False, default="local")  # local, google, facebook, apple
    provider_user_id = Column(String(255), nullable=True)
    is_email_verified = Column(Boolean, default=False)
    role = Column(String(20), default="user")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    detail = relationship(
        "UserDetail",
        uselist=False,
        back_populates="user",
        lazy="joined",
        cascade="all, delete-orphan",
    )
