from fastapi import HTTPException, status

from app.database.models.user import User


async def check_existing_user(email: str) -> bool:
    user = await User.find_one(User.email == email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User {email} already exists, please login"
        )
    return True