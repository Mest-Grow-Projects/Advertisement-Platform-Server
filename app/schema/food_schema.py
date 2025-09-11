from pydantic import BaseModel
from app.database.models.food import FoodCategory
from typing import Annotated
from fastapi import File, UploadFile


class FoodSchema(BaseModel):
    name: str
    description: str
    category: FoodCategory
    price: float
    image: Annotated[UploadFile, File()]
