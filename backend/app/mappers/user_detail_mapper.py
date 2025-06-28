from app.models.user_detail import UserDetail
from app.schemas.user_detail_schema import (
    UserDetailCreate,
    UserDetailUpdate,
    UserDetailRead,
)


class UserDetailMapper:
    @staticmethod
    def to_read(model: UserDetail) -> UserDetailRead:
        return UserDetailRead.from_orm(model)

    @staticmethod
    def from_create(user_id: int, data: UserDetailCreate) -> UserDetail:
        return UserDetail(
            user_id=user_id,
            name=data.name,
            active_language_pair_id=data.active_language_pair_id,
        )

    @staticmethod
    def update_model(model: UserDetail, data: UserDetailUpdate) -> UserDetail:
        if data.name is not None:
            model.name = data.name
        if data.active_language_pair_id is not None:
            model.active_language_pair_id = data.active_language_pair_id
        return model
