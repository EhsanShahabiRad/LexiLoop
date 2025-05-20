from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.user_schema import UserCreate, UserRead
from app.services.user_service import UserService
from app.repositories.implementations.pg_user_repository import PGUserRepository
from app.db.session import get_db

router = APIRouter()

user_repository = PGUserRepository()
user_service = UserService(user_repository)


@router.post("/signup", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    existing_user = user_service.get_user_by_email(db, user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    user = user_service.register_user(db, user_in)
    return user
