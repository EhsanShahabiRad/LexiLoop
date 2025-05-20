from abc import ABC, abstractmethod
from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user_schema import UserCreate


class IUserRepository(ABC):
    @abstractmethod
    def get_by_id(self, db: Session, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def create(self, db: Session, user_in: UserCreate) -> User:
        pass

    @abstractmethod
    def update(self, db: Session, user_id: int, updates: dict) -> Optional[User]:
        pass

    @abstractmethod
    def delete(self, db: Session, user_id: int) -> bool:
        pass
