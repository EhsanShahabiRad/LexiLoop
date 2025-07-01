from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from jose import jwt, JWTError

from app.db.session import get_db
from app.core.jwt import create_access_token, create_refresh_token
from app.core.config import settings
from app.models.user import User
from app.repositories.implementations.pg_user_repository import PGUserRepository
from app.repositories.implementations.pg_user_detail_repository import PgUserDetailRepository

router = APIRouter()
GOOGLE_CLIENT_ID = settings.google_client_id


class GoogleLoginRequest(BaseModel):
    id_token: str


@router.post("/google-login")
async def google_login(payload: GoogleLoginRequest, db: AsyncSession = Depends(get_db)):
    try:
        idinfo = id_token.verify_oauth2_token(
            payload.id_token,
            google_requests.Request(),
            GOOGLE_CLIENT_ID,
        )

        email = idinfo["email"]
        provider_user_id = idinfo.get("sub")

        user_repo = PGUserRepository(db)
        user = await user_repo.get_by_email(email)

        if not user:
            user = User(
                email=email,
                is_email_verified=True,
                auth_provider="google",
                provider_user_id=provider_user_id,
            )
            user = await user_repo.create(user)

        detail_repo = PgUserDetailRepository(db)
        detail = await detail_repo.get_user_detail_by_user_id(user.id)
        source_lang_id = detail.source_language_id if detail else None
        target_lang_id = detail.target_language_id if detail else None
        name = detail.name if detail else None

        access_token = create_access_token(user.id, source_lang_id, target_lang_id, name)
        refresh_token = create_refresh_token(user.id)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    except Exception as e:
        print(f"❌ Google login failed: {e}")
        raise HTTPException(status_code=401, detail="Invalid Google Token")


class RefreshTokenRequest(BaseModel):
    refresh_token: str


@router.post("/refresh-token")
async def refresh_access_token(
    payload: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        decoded = jwt.decode(payload.refresh_token, settings.secret_key, algorithms=[settings.algorithm])

        if decoded.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")

        if datetime.utcnow().timestamp() > decoded["exp"]:
            raise HTTPException(status_code=401, detail="Refresh token expired")

        user_id = int(decoded["sub"])

        user_repo = PGUserRepository(db)
        user = await user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        detail_repo = PgUserDetailRepository(db)
        detail = await detail_repo.get_user_detail_by_user_id(user_id)

        source_lang_id = detail.source_language_id if detail else None
        target_lang_id = detail.target_language_id if detail else None
        name = detail.name if detail else None

        new_access_token = create_access_token(
            user_id=user.id,
            source_lang_id=source_lang_id,
            target_lang_id=target_lang_id,
            name=name,
        )

        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }

    except (JWTError, ValueError, TypeError) as e:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")





# from fastapi import APIRouter, HTTPException, Depends
# from pydantic import BaseModel
# from google.oauth2 import id_token
# from google.auth.transport import requests as google_requests
# from sqlalchemy.ext.asyncio import AsyncSession
# from app.db.session import get_db
# from app.core.jwt import create_access_token, create_refresh_token
# from app.core.config import settings
# from app.models.user import User
# from app.repositories.implementations.pg_user_repository import PGUserRepository
# from app.repositories.implementations.pg_user_detail_repository import PgUserDetailRepository
# from jose import jwt, JWTError
# from datetime import datetime


# router = APIRouter()
# GOOGLE_CLIENT_ID = settings.google_client_id


# class GoogleLoginRequest(BaseModel):
#     id_token: str


# @router.post("/google-login")
# async def google_login(payload: GoogleLoginRequest, db: AsyncSession = Depends(get_db)):
#     try:
#         idinfo = id_token.verify_oauth2_token(
#             payload.id_token,
#             google_requests.Request(),
#             GOOGLE_CLIENT_ID,
#         )

#         email = idinfo["email"]
#         provider_user_id = idinfo.get("sub")

#         user_repo = PGUserRepository(db)
#         user = await user_repo.get_by_email(email)

#         if not user:
#             user = User(
#                 email=email,
#                 is_email_verified=True,
#                 auth_provider="google",
#                 provider_user_id=provider_user_id,
#             )
#             user = await user_repo.create(user)

#         detail_repo = PgUserDetailRepository(db)
#         detail = await detail_repo.get_user_detail_by_user_id(user.id)
#         source_lang_id = detail.source_language_id if detail else None
#         target_lang_id = detail.target_language_id if detail else None

#         access_token = create_access_token(user.id, source_lang_id, target_lang_id)
#         refresh_token = create_refresh_token(user.id)

#         return {
#             "access_token": access_token,
#             "refresh_token": refresh_token,
#             "token_type": "bearer"
#         }

#     except Exception as e:
#         print(f"❌ Google login failed: {e}")
#         raise HTTPException(status_code=401, detail="Invalid Google Token")

# class RefreshTokenRequest(BaseModel):
#     refresh_token: str


# @router.post("/refresh-token")
# async def refresh_token(
#     payload: RefreshTokenRequest,
#     db: AsyncSession = Depends(get_db),
# ):
#     try:
#         decoded = jwt.decode(payload.refresh_token, settings.secret_key, algorithms=[settings.algorithm])

#         if decoded.get("type") != "refresh":
#             raise HTTPException(status_code=401, detail="Invalid token type")

#         if datetime.utcnow().timestamp() > decoded["exp"]:
#             raise HTTPException(status_code=401, detail="Refresh token expired")

#         user_id = int(decoded["sub"])

#         user_repo = PGUserRepository(db)
#         user = await user_repo.get_by_id(user_id)
#         if not user:
#             raise HTTPException(status_code=404, detail="User not found")

#         detail_repo = PgUserDetailRepository(db)
#         detail = await detail_repo.get_user_detail_by_user_id(user_id)

#         source_lang_id = detail.source_language_id if detail else None
#         target_lang_id = detail.target_language_id if detail else None
#         name = detail.name if detail else None

#         new_access_token = create_access_token(
#             user_id=user.id,
#             source_lang_id=source_lang_id,
#             target_lang_id=target_lang_id,
#             name=name,
#         )

#         return {
#             "access_token": new_access_token,
#             "token_type": "bearer"
#         }

#     except (JWTError, ValueError, TypeError) as e:
#         raise HTTPException(status_code=401, detail="Invalid or expired refresh token")