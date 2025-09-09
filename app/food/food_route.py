from fastapi import APIRouter, Form, File, UploadFile, HTTPException, status
from app.schema.food_schema import FoodSchema
from app.database.models.food import Food


router = APIRouter(tags=["Food"])


@router.post("/food_ad")
def post_food_ads(data: FoodSchema):
    food = Food(
        name=data.name,
        description=data.description,
        category=data.category,
        price=data.price,
    )
    food.insert()
    return {"message": "You have successfully added an ad"}
