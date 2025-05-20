from sqlalchemy.orm import Session
from typing import Optional
from passlib.context import CryptContext
from app.models.user import User
from app.schemas.user_schema import UserCreate
from app.repositories.interfaces.i_user_repository import IUserRepository


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def get_user_by_id(self, db: Session, user_id: int) -> Optional[User]:
        return self.user_repository.get_by_id(db, user_id)

    def get_user_by_email(self, db: Session, email: str) -> Optional[User]:
        return self.user_repository.get_by_email(db, email)

    def register_user(self, db: Session, user_in: UserCreate) -> User:
        return self.user_repository.create(db, user_in)


    def update_user(self, db: Session, user_id: int, updates: dict) -> Optional[User]:
        return self.user_repository.update(db, user_id, updates)

    def delete_user(self, db: Session, user_id: int) -> bool:
        return self.user_repository.delete(db, user_id)

    def _hash_password(self, plain_password: str) -> str:
        return pwd_context.hash(plain_password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
