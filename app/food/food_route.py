from fastapi import APIRouter, Form, File, UploadFile, HTTPException, status
from app.schema.food_schema import FoodSchema
from app.database.models.food import Food


router = APIRouter(tags=["Food"])


@router.post("/food_ad")
async def post_food_ads(data: FoodSchema):
    food = Food(
        name=data.name,
        description=data.description,
        category=data.category,
        price=data.price,
    )
    await food.insert()
    return {"message": "You have successfully added an ad"}


@router.get("/all")
async def get_all_food_ads(limit=10, skip=0):
    foods = await Food.find(
        # filter={
        #     "$or": [
        #         {"name": {"$regex": data.name, "$options": "i"}},
        #         {"description": {"$regex": data.description, "$options": "i"}},
        #     ]
        # },
        # limit=int(limit),
        # skip=int(skip),
    ).to_list()
    return {"data": foods}


@router.delete("/{food_id}")
async def delete_food_ad(food_id):
    if not food_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Food ID required")
    deleted_ad = await Food.find(food_id)
    if not deleted_ad:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Food not found")
    await Food.delete_one(food_id)
    return {"message": "Ad successfully deleted!"}
