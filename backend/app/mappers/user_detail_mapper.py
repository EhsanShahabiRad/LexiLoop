from typing import Optional
from app.models.user_detail import UserDetail
from app.schemas.user_detail_schema import (
    UserDetailUpdate,
    UserDetailRead,
)


class UserDetailMapper:
    @staticmethod
    def to_read(model: UserDetail) -> UserDetailRead:
        return UserDetailRead.model_validate(model)

    @staticmethod
    def from_create(user_id: int, name: Optional[str], source_lang_id: Optional[int], target_lang_id: Optional[int]) -> UserDetail:
        return UserDetail(
            user_id=user_id,
            name=name,
            source_language_id=source_lang_id,
            target_language_id=target_lang_id,
        )

    @staticmethod
    def update_model(model: UserDetail, data: UserDetailUpdate) -> UserDetail:
        if data.name is not None:
            model.name = data.name
        if data.source_language_id is not None:
            model.source_language_id = data.source_language_id
        if data.target_language_id is not None:
            model.target_language_id = data.target_language_id
        return model
