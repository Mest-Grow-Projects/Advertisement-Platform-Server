from fastapi import APIRouter, Form, File, UploadFile, HTTPException, status
from app.schema.food_schema import FoodSchema, FilterQuery
from app.database.models.food import Food, FoodCategory
import cloudinary
import cloudinary.uploader
from typing import Annotated
from app.config.config import get_settings


settings = get_settings()
cloudinary.config(
    cloud_name=settings.CLOUD_NAME,
    api_key=settings.API_KEY,
    api_secret=settings.API_SECRET
)


router = APIRouter(tags=["Food"])


@router.post("/food_ads")
async def post_food_ads(name: Annotated[str, Form()],
    description: Annotated[str, Form()],
    category: Annotated[FoodCategory, Form()],
    price: Annotated[float, Form()],
    image: Annotated[UploadFile, File()]
):
    upload_result = cloudinary.uploader.upload(image.file)
    food = Food(
        name=name,
        description=description,
        category=category,
        price=price,
        image=upload_result["secure_url"],
    )

    await food.insert()
    return {"message": "You have successfully added an ad"}


@router.get("/all")
async def get_all_food_ads(filter_query: FilterQuery):
    skip = (filter_query.page - 1) * filter_query.limit
    query = {}

    if filter_query.name:
        query["name"] = {"$regex": filter_query.name, "$options": "i"}
    if filter_query.price:
        query["price"] = {"$regex": filter_query.price, "$options": "i"}
    if filter_query.ratings:
        query["ratings"] = {"$regex": filter_query.ratings, "$options": "i"}
    if filter_query.category:
        query["category"] = filter_query.category.value
    if filter_query.nutrition:
        query["nutrition"] = filter_query.nutrition.value


    total_food_count = await Food.find(query).count()
    food_ads = (
        await Food.find(query)
        .sort(f"-{filter_query.order_by}")
        .skip(skip)
        .limit(filter_query.limit)
        .to_list()
    )
    return {
        "message": "food ads retrieved successfully",
        "data": food_ads,
        "pagination": {
            "total": total_food_count,
            "page": filter_query.page,
            "limit": filter_query.limit,
            "total_pages": (total_food_count + filter_query.limit - 1) // filter_query.limit,
        }
    }


@router.get("/{food_id}")
async def get_one_ad(food_id):
    if not food_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Food ID required")
    get_one = await Food.get(food_id)
    if not get_one:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Food not found")
    return {"message": get_one}


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
    return {"message": "Food ad updated successfully!"}


@router.delete("/{food_id}")
async def delete_food_ad(food_id):
    if not food_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Food ID required")
    deleted_ad = await Food.get(food_id)
    if not deleted_ad:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Food not found")
    await deleted_ad.delete()
    return {"message": "Ad successfully deleted!"}