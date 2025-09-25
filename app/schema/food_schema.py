from typing import Literal
from pydantic import BaseModel, Field
from app.database.models.food import FoodCategory, Nutrition


class FoodSchema(BaseModel):
    name: str
    description: str
    category: FoodCategory
    price: float
    ratings: float

    model_config = {"extra": "forbid"}


class FilterQuery(BaseModel):
    name: str | None = None
    price: float | None = None
    category: FoodCategory | None = None
    ratings: float | None = None
    order_by: Literal["created_at", "updated_at"] = "created_at"
    page: int = Field(1, ge=1)
    limit: int = Field(20, ge=1, le=50)

    model_config = {"extra": "forbid"}