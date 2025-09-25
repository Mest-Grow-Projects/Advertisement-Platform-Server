from fastapi import HTTPException, status
from app.schema.user_schema import SignupSchema, LoginSchema
from app.database.repository.user_repo import (
    check_existing_user,
    create_user,
    get_user_by_email,
)
from app.config.password_hash import verify_password
from datetime import datetime, timezone, timedelta
import jwt
from app.config.config import get_settings

settings = get_settings()


class AuthService:
    async def signup(self, user: SignupSchema):
        await check_existing_user(str(user.email))
        new_user = await create_user(user)

        return {
            "message": "User registered successfully",
            "data": {
                "name": new_user.name,
                "email": new_user.email,
                "role": new_user.role,
            },
        }

    async def login(self, user: LoginSchema):
        found_user = await get_user_by_email(str(user.email))
        password_valid = verify_password(user.password, found_user.password)

        if not found_user or not password_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email or password",
            )
        access_token = jwt.encode(
            {
                "id": str(found_user.id),
                "role": found_user.role,
                "exp": datetime.now(tz=timezone.utc) + timedelta(days=60),
            },
            settings.JWT_SECRET_KEY,
            "HS256",
        )

        return {
            "message": "User logged in successfully",
            "data": {
                "name": found_user.name,
                "email": found_user.email,
                "role": found_user.role,
                "access_token": access_token,
            },
        }


auth_service = AuthService()
