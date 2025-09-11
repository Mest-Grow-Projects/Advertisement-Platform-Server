from beanie import Document
from enum import Enum
from datetime import datetime, timezone
from pydantic import Field
import pymongo


class FoodCategory(str, Enum):
    BEVERAGES = ("beverages",)
    SNACKS = ("snacks",)
    BREAKFAST = ("breakfast",)
    LUNCH = ("lunch",)
    DINNER = ("dinner",)
    FAST_FOOD = "fast_food"


class Nutrition(str, Enum):
    CALORIES = ("calories",)
    PROTEINS = ("proteins",)
    FATS = ("fats",)
    CARBOHYDRATES = "carbohydrates"
    VITAMINS = "vitamins"


class Food(Document):
    name: str
    image: str | None = None
    category: FoodCategory
    price: float
    description: str
    ratings: float | None = None
    nutrition: Nutrition | None = None
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updatedAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "foods"
        indexes = [
            [("createdAt", pymongo.DESCENDING)],
            [("price", pymongo.ASCENDING)],
            [("ratings", pymongo.ASCENDING)],
        ]
