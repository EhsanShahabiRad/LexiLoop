from sqlalchemy.orm import Session
from typing import Optional
from app.models.user import User
from app.schemas.user_schema import UserCreate
from app.repositories.interfaces.i_user_repository import IUserRepository


class PGUserRepository(IUserRepository):
    def get_by_id(self, db: Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, user_in: UserCreate) -> User:
        user = User(
            email=user_in.email,
            password_hash=None  
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user


    def update(self, db: Session, user_id: int, updates: dict) -> Optional[User]:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        for key, value in updates.items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return user

    def delete(self, db: Session, user_id: int) -> bool:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        db.delete(user)
        db.commit()
        return True
