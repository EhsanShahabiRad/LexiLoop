from sqlalchemy import Column, Integer, String
from app.db.base_class import Base

class Language(Base):
    __tablename__ = "languages"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(10), unique=True, nullable=False)  # e.g., "en", "de"
    name = Column(String(50), nullable=False)               # e.g., "English", "Deutsch"
