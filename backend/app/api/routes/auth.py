from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.jwt import create_access_token
from app.core.config import settings
from app.models.user import User
from app.repositories.implementations.pg_user_repository import PGUserRepository

router = APIRouter()
GOOGLE_CLIENT_ID = settings.google_client_id


class GoogleLoginRequest(BaseModel):
    id_token: str


@router.post("/google-login")
async def google_login(payload: GoogleLoginRequest, db: AsyncSession = Depends(get_db)):
    print("📥 Received request to /auth/google-login")
    print(f"🔸 Incoming id_token: {payload.id_token[:20]}...")

    try:
        idinfo = id_token.verify_oauth2_token(
            payload.id_token,
            google_requests.Request(),
            GOOGLE_CLIENT_ID,
        )

        print("✅ id_token verified successfully")

        email = idinfo["email"]
        provider_user_id = idinfo.get("sub")

        print(f"🔸 Email from token: {email}")
        print(f"🔸 Provider user ID: {provider_user_id}")

        user_repository = PGUserRepository(db)
        user = await user_repository.get_by_email(email)

        if user:
            print("ℹ️ User already exists in DB")
        else:
            print("🆕 Creating new user in DB")
            user = User(
                email=email,
                is_email_verified=True,
                auth_provider="google",
                provider_user_id=provider_user_id,
            )
            user = await user_repository.create(user)
            print(f"✅ New user created with ID: {user.id}")

        access_token = create_access_token(subject=str(user.id))
        print(f"🎟️ JWT issued: {access_token[:20]}...")

        return {"access_token": access_token, "token_type": "bearer"}

    except Exception as e:
        print(f"❌ Exception in google_login: {e}")
        raise HTTPException(status_code=401, detail="Invalid Google Token")







# from fastapi import APIRouter, HTTPException, Depends
# from pydantic import BaseModel
# from google.oauth2 import id_token
# from google.auth.transport import requests as google_requests
# from sqlalchemy.ext.asyncio import AsyncSession
# from app.db.session import get_db
# from app.core.jwt import create_access_token
# from app.core.config import settings
# from app.models.user import User
# from app.repositories.implementations.pg_user_repository import PGUserRepository

# router = APIRouter()
# GOOGLE_CLIENT_ID = settings.google_client_id


# class GoogleLoginRequest(BaseModel):
#     id_token: str


# @router.post("/google-login")
# async def google_login(payload: GoogleLoginRequest, db: AsyncSession = Depends(get_db)):
#     print("📥 Received request to /auth/google-login")
#     print(f"🔸 Incoming id_token: {payload.id_token[:20]}...")

#     try:
#         idinfo = id_token.verify_oauth2_token(
#             payload.id_token,
#             google_requests.Request(),
#             GOOGLE_CLIENT_ID,
#         )

#         print("✅ id_token verified successfully")

#         email = idinfo["email"]
#         provider_user_id = idinfo.get("sub")

#         print(f"🔸 Email from token: {email}")
#         print(f"🔸 Provider user ID: {provider_user_id}")

#         user_repository = PGUserRepository(db)
#         user = await user_repository.get_by_email(email)

#         if user:
#             print("ℹ️ User already exists in DB")
#         else:
#             print("🆕 Creating new user in DB")
#             user = User(
#                 email=email,
#                 is_email_verified=True,
#                 auth_provider="google",
#                 provider_user_id=provider_user_id,
#             )
#             user = await user_repository.create(user)
#             print(f"✅ New user created with ID: {user.id}")

#         access_token = create_access_token(subject=str(user.id))
#         print(f"🎟️ JWT issued: {access_token[:20]}...")

#         return {"access_token": access_token, "token_type": "bearer"}

#     except Exception as e:
#         print(f"❌ Exception in google_login: {e}")
#         raise HTTPException(status_code=401, detail="Invalid Google Token")




# from fastapi import APIRouter, HTTPException, Depends
# from pydantic import BaseModel
# from google.oauth2 import id_token
# from google.auth.transport import requests as google_requests
# from sqlalchemy.ext.asyncio import AsyncSession
# from app.db.session import get_db
# from app.core.jwt import create_access_token
# from app.core.config import settings
# from app.models.user import User
# from app.repositories.implementations.pg_user_repository import PGUserRepository

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

#         user_repository = PGUserRepository(db)
#         user = await user_repository.get_by_email(email)

#         if not user:
#             user = User(
#                 email=email,
#                 is_email_verified=True,
#                 auth_provider="google",
#                 provider_user_id=provider_user_id,
#             )
#             user = await user_repository.create(user)

#         if not user:
#             raise HTTPException(status_code=500, detail="User creation failed")

#         access_token = create_access_token(subject=str(user.id))
#         return {"access_token": access_token, "token_type": "bearer"}

#     except Exception as e:
        
#         print(f"[auth/google-login] ❌ Exception: {type(e).__name__}: {e}")
#         raise HTTPException(status_code=401, detail="Invalid Google Token")
