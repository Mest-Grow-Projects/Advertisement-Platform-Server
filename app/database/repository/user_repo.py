from fastapi import HTTPException, status
from app.database.models.user import User
from app.schema.user_schema import SignupSchema
from pydantic import BaseModel
from app.config.password_hash import PasswordHash


async def check_existing_user(email: str) -> bool:
    user = await User.find_one(User.email == email.lower())
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User {email} already exists, please login",
        )
    return False


async def get_user_by_id(user_id: str) -> User:
    user = await User.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found, please register",
        )
    return user


async def get_user_by_email(email: str) -> User:
    user = await User.find_one(User.email == email.lower())
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found, please register",
        )
    return user


async def create_user(user_data: SignupSchema) -> User:
    hashed_password = PasswordHash.get_password_hash(user_data.password)
    new_user = User(
        name=user_data.name,
        email=str(user_data.email),
        password=hashed_password,
        role=user_data.role,
    )
    await new_user.insert()

    if not new_user.id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user, please try again",
        )
    return new_user


async def get_and_validate_user(user_id: str) -> User:
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User ID is required",
        )
    user = await get_user_by_id(user_id)
    return user


def validate_updated_data(data: BaseModel):
    updated_data = data.model_dump(exclude_unset=True, exclude_none=True)

    if not updated_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided for update",
        )
    return updated_data
