from beanie import init_beanie
from pymongo import AsyncMongoClient
from app.config.config import get_settings
from app.database.models.user import User
from app.database.models.food import Food
from dotenv import load_dotenv
import os


settings = get_settings()
mongo_client = None

async def init_db():
    global mongo_client
    load_dotenv()
    db_connection_string = os.getenv("DATABASE_URI")
    db_name = "Food_Ad"

    if not db_connection_string:
        raise ValueError('DATABASE_URI is not set in environment variables')

    mongo_client = AsyncMongoClient(db_connection_string)
    database = mongo_client[db_name]
    await init_beanie(
        database=database,
        document_models=[User, Food]
    )