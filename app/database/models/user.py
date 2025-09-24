from datetime import datetime, timezone
from typing import Annotated
from beanie import Document, Indexed
from enum import Enum
from pydantic import Field
import pymongo


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    NON_BINARY = "non-binary"


class Roles(str, Enum):
    ADMIN = "admin"
    VENDOR = "vendor"
    USER = "user"


class User(Document):
    name: str
    email: Annotated[str, Indexed(unique=True)]
    password: str
    address: str | None = None
    phone_number: str | None = None
    gender: Gender | None = None
    role: Roles
    profile_image: str | None = None
    dob: datetime | None = None
    bio: str | None = None
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updatedAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "users"
        indexes = [[("createdAt", pymongo.DESCENDING)]]
