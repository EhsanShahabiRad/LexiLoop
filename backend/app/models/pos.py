from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class POS(Base):
    __tablename__ = "pos"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30), nullable=False)

    meanings = relationship("Meaning", back_populates="pos")
