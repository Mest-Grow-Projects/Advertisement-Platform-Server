from pydantic import BaseModel
from app.database.models.food import FoodCategory


class FoodSchema(BaseModel):
    name: str
    description: str
    category: FoodCategory
    price: float
