from fastapi import APIRouter, Form, File, UploadFile, HTTPException, status
from app.schema.food_schema import FoodSchema
from app.database.models.food import Food

# from app.database.models.food import cloudinary
# from app.database.models.food import cloudinary.uploader


# cloudinary.config(
#     cloud_name="dwlfbnmis",
#     api_key="635478319253588",
#     api_secret="O7D2CmW2S6J5oUFteftbGvmJxpE",
# )

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
    deleted_ad = await Food.get(food_id)
    if not deleted_ad:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Food not found")
    await deleted_ad.delete()
    return {"message": "Ad successfully deleted!"}


@router.put("/food_ad/{food_id}")
async def update_food_ad(food_id, data: FoodSchema):
    if not food_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Food ID required")

    update_ad = await Food.get(food_id)
    if not update_ad:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Food not found")

    updated_data = data.model_dump()
    if not updated_data:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid input")

    await update_ad.set(updated_data)
    return {"message": "Food ad upadated successfully!"}


@router.get("/{food_id}")
async def get_one_ad(food_id):
    if not food_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Food ID required")
    get_one = await Food.get(food_id)
    if not get_one:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Food not found")
    await get_one.get(food_id)
    return {"message": f"{get_one}"}
