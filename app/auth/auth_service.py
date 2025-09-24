from fastapi import HTTPException, status

from app.schema.user_schema import SignupSchema, LoginSchema
from app.database.repository.user_repo import (
    check_existing_user,
    create_user,
    get_user_by_id,
    get_user_by_email
)
from app.config.password_hash import PasswordHash

class AuthService:
    async def signup(self, user: SignupSchema):
        await check_existing_user(str(user.email))
        new_user = await create_user(user)

        return {
            'message': "User registered successfully",
            'data': {
                'name': new_user.name,
                'email': new_user.email,
            },
        }


    async def login(self, user: LoginSchema):
        found_user = await get_user_by_email(str(user.email))
        password_valid = PasswordHash.verify_password(user.password, found_user.password)

        if not found_user or not password_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email or password"
            )

        return {
            'message': "User logged in successfully",
            'data': {
                'name': found_user.name,
                'email': found_user.email,
            },
        }



auth_service = AuthService()