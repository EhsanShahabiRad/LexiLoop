from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user_profile_schema import UserProfileRead, UserProfileUpdate
from app.dependencies.user_service import get_user_service
from app.dependencies.user_detail_repository import get_user_detail_repository
from app.dependencies.language_pair_repository import get_language_pair_repository
from app.core.jwt import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.services.user_service import UserService
from app.repositories.interfaces.i_user_detail_repository import IUserDetailRepository
from app.repositories.interfaces.i_language_pair_repository import ILanguagePairRepository
from app.dependencies.validators.profile_validators import validate_profile_update


router = APIRouter()


@router.get("/me/profile", response_model=UserProfileRead)
async def get_profile(
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
    user_detail_repo: IUserDetailRepository = Depends(get_user_detail_repository),
    language_pair_repo: ILanguagePairRepository = Depends(get_language_pair_repository),
):
    user_detail = await user_detail_repo.get_user_detail_by_user_id(current_user.id)

    active_language_pair_id = None
    if user_detail and user_detail.source_language_id and user_detail.target_language_id:
        pair = await language_pair_repo.get_by_langs(
            source_lang_id=user_detail.source_language_id,
            target_lang_id=user_detail.target_language_id,
        )
        active_language_pair_id = pair.id if pair else None

    return UserProfileRead(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username,
        name=user_detail.name if user_detail else None,
        active_language_pair_id=active_language_pair_id,
        created_at=current_user.created_at,
    )


@router.put("/me/profile", response_model=UserProfileRead)
async def update_profile(
    update: UserProfileUpdate = Depends(validate_profile_update),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    user_service: UserService = Depends(get_user_service),
    user_detail_repo: IUserDetailRepository = Depends(get_user_detail_repository),
    language_pair_repo: ILanguagePairRepository = Depends(get_language_pair_repository),
):
    # Update user and profile with validation
    await user_service.update_profile(
        db=db,
        current_user=current_user,
        update=update,
        user_detail_repo=user_detail_repo,
        language_pair_repo=language_pair_repo,
    )

    # Fetch updated data
    updated_user = await user_service.get_user_by_id(current_user.id)
    updated_detail = await user_detail_repo.get_user_detail_by_user_id(current_user.id)

    active_language_pair_id = None
    if updated_detail and updated_detail.source_language_id and updated_detail.target_language_id:
        pair = await language_pair_repo.get_by_langs(
            source_lang_id=updated_detail.source_language_id,
            target_lang_id=updated_detail.target_language_id,
        )
        active_language_pair_id = pair.id if pair else None

    return UserProfileRead(
        id=updated_user.id,
        email=updated_user.email,
        username=updated_user.username,
        name=updated_detail.name if updated_detail else None,
        active_language_pair_id=active_language_pair_id,
        created_at=updated_user.created_at,
    )
