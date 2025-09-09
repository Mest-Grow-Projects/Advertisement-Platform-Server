from fastapi import HTTPException, status

from app.database.models.user import User


async def check_existing_user(email: str) -> bool:
    user = await User.find_one(User.email == email.lower())
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User {email} already exists, please login"
        )
    return False


async def get_user_by_id(user_id: str) -> User:
    user = await User.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found, please register"
        )
    return user


