from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.core.jwt import create_access_token 
from app.core.config import settings
from app.models.user import User
from app.repositories.implementations.pg_user_repository import PGUserRepository

router = APIRouter()
GOOGLE_CLIENT_ID = settings.google_client_id

class GoogleLoginRequest(BaseModel):
    id_token: str

@router.post("/auth/google-login")
def google_login(payload: GoogleLoginRequest, db: Session = Depends(get_db)):
    try:
        idinfo = id_token.verify_oauth2_token(
            payload.id_token,
            google_requests.Request(),
            GOOGLE_CLIENT_ID,
        )

        email = idinfo["email"]
        provider_user_id = idinfo.get("sub")

        user_repository = PGUserRepository(db)
        user = user_repository.get_by_email(email)

        if not user:
            user = User(
                email=email,
                is_email_verified=True,
                auth_provider="google",
                provider_user_id=provider_user_id
            )
            user = user_repository.create(user)

        access_token = create_access_token(subject=str(user.id))
        return {"access_token": access_token, "token_type": "bearer"}

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Google Token")
