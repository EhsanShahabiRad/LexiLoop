from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user_profile_schema import UserProfileRead, UserProfileUpdate
from app.dependencies.user_service import get_user_service
from app.dependencies.user_detail_repository import get_user_detail_repository
from app.core.jwt import get_current_user
from app.models.user import User
from app.services.user_service import UserService
from app.repositories.interfaces.i_user_detail_repository import IUserDetailRepository

router = APIRouter()


@router.get("/me/profile", response_model=UserProfileRead)
async def get_profile(
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
    user_detail_repo: IUserDetailRepository = Depends(get_user_detail_repository),
):
    user_detail = await user_detail_repo.get_user_detail_by_user_id(current_user.id)

    return UserProfileRead(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username,
        name=user_detail.name if user_detail else None,
        active_language_pair_id=user_detail.active_language_pair_id if user_detail else None,
        created_at=current_user.created_at,
    )


@router.put("/me/profile", response_model=UserProfileRead)
async def update_profile(
    update: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
    user_detail_repo: IUserDetailRepository = Depends(get_user_detail_repository),
):
    await user_service.update_user(current_user.id, update)

    user_detail = await user_detail_repo.get_user_detail_by_user_id(current_user.id)
    if user_detail:
        await user_detail_repo.update_user_detail(current_user.id, update)
    else:
        await user_detail_repo.create_user_detail(current_user.id, update)

    updated_user = await user_service.get_user_by_id(current_user.id)
    updated_detail = await user_detail_repo.get_user_detail_by_user_id(current_user.id)

    return UserProfileRead(
        id=updated_user.id,
        email=updated_user.email,
        username=updated_user.username,
        name=updated_detail.name if updated_detail else None,
        active_language_pair_id=updated_detail.active_language_pair_id if updated_detail else None,
        created_at=updated_user.created_at,
    )
