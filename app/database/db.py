from beanie import init_beanie
from app.database.models.user import User
from app.database.models.food import Food
from dotenv import load_dotenv
import os
from motor.motor_asyncio import AsyncIOMotorClient

mongo_client = None

async def init_db():
    global mongo_client
    load_dotenv()
    db_connection_string = os.getenv("DATABASE_URI")
    db_name = "Food_Ad"

    if not db_connection_string:
        raise ValueError('DATABASE_URI is not set in environment variables')

    mongo_client = AsyncIOMotorClient(
        db_connection_string,
        serverSelectionTimeoutMS=30000,  # 30 seconds
        connectTimeoutMS=30000,
        socketTimeoutMS=30000,
        maxPoolSize=10,
        retryWrites=True
    )

    print(f"Connecting to database: {db_name}")
    print(f"Connection string starts with: {db_connection_string[:20]}...")
    database = mongo_client[db_name]

    await init_beanie(
        database=database,
        document_models=[User, Food]
    )