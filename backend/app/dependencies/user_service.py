from fastapi import Depends
from app.dependencies.user_repository import get_user_repository
from app.repositories.interfaces.i_user_repository import IUserRepository
from app.services.user_service import UserService

def get_user_service(user_repo: IUserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(user_repo)
