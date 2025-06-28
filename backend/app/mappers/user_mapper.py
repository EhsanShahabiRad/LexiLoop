from typing import Optional
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserUpdate, UserRead
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserMapper:
    @staticmethod
    def to_model(data: UserCreate, hashed_password: Optional[str] = None) -> User:
        return User(
            email=data.email,
            username=data.username,
            password_hash=hashed_password,
            auth_provider=data.auth_provider,
            provider_user_id=data.provider_user_id,
        )

    @staticmethod
    def to_read(user: User) -> UserRead:
        return UserRead.from_orm(user)

    @staticmethod
    def update_model(user: User, data: UserUpdate) -> User:
        if data.email is not None:
            user.email = data.email
        if data.username is not None:
            user.username = data.username
        if data.is_email_verified is not None:
            user.is_email_verified = data.is_email_verified
        if data.role is not None:
            user.role = data.role
        return user

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
