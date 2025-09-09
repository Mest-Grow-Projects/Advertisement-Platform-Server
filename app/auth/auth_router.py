from .auth_service import auth_service
from fastapi import APIRouter
from app.schema.user_schema import LoginSchema, SignupSchema

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.post(
    "/signup",
    summary="User registration"
)
async def signup(user: SignupSchema):
    return await auth_service.login(user)


@router.post(
    "/login",
    summary="User login"
)
async def login(user: LoginSchema):
    return await auth_service.login(user)