from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.repositories.implementations.pg_user_repository import PGUserRepository
from app.repositories.interfaces.i_user_repository import IUserRepository

def get_user_repository(db: Session = Depends(get_db)) -> IUserRepository:
    return PGUserRepository(db)
