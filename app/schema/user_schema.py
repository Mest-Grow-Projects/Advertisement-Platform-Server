from pydantic import BaseModel, EmailStr, Field
from app.database.models.user import Roles


class SignupSchema(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=50,
        pattern=r"^[a-zA-Z]+(?: [a-zA-Z]+)*$",
        description="Name must contain only letters and single spaces between words, no numbers or special characters allowed",
    )
    email: EmailStr
    password: str = Field(
        min_length=5,
        description="Password must contain at least five character",
    )
    role: Roles

    # confirm_password: str = Field(
    #     min_length=8,
    #     description="Must match the password field",
    # )

    # @field_validator("password")
    # @classmethod
    # def validate_password(cls, value: str) -> str:
    #     if not re.search(r"[a-z]", value):
    #         raise ValueError("Password must contain at least one lowercase letter")
    #     if not re.search(r"[A-Z]", value):
    #         raise ValueError("Password must contain at least one uppercase letter")
    #     if not re.search(r"\d", value):
    #         raise ValueError("Password must contain at least one digit")
    #     if not re.search(r"[@$!%*?&]", value):
    #         raise ValueError("Password must contain at least one special character (@, $, !, %, *, ?, &)")
    #     return value

    # @model_validator(mode='after')
    # def check_password_match(self) -> 'SignupSchema':
    #     if self.password != self.confirm_password:
    #         raise ValueError("Password and Confirm Password do not match")
    #     return self

    model_config = {"extra": "forbid"}


class LoginSchema(BaseModel):
    email: EmailStr
    password: str = Field(
        min_length=5,
        description="Password must contain at least five character",
    )
    model_config = {"extra": "forbid"}
