import regex as re
from fastapi import HTTPException
from app.schemas.user_profile_schema import UserProfileUpdate
from fastapi import Body

NAME_REGEX = re.compile(r"^[\p{L} ]+$")

async def validate_profile_update(update: UserProfileUpdate = Body(...)) -> UserProfileUpdate:
    # Normalize email
    if update.email:
        update.email = update.email.strip().lower()

    # Username is required
    if not update.username:
        raise HTTPException(status_code=400, detail="Username is required.")
    if len(update.username) < 5 or len(update.username) > 20:
        raise HTTPException(status_code=400, detail="Username must be 5–20 characters.")

    if not re.fullmatch(r"^(?![_.-])(?!.*[_.-]{2})(?!.*[_.-]$)[a-zA-Z0-9_.-]+$", update.username):
        raise HTTPException(status_code=400, detail="Username has invalid characters or format.")

    # Name (optional)
    if update.name is not None:
        stripped = update.name.strip()
        if len(stripped) < 2 or len(stripped) > 50:
            raise HTTPException(status_code=400, detail="Name must be 2–50 characters.")
        if not NAME_REGEX.fullmatch(stripped):
            raise HTTPException(status_code=400, detail="Name can only contain letters and spaces.")
        update.name = stripped

    return update
