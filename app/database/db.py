from beanie import init_beanie
from pymongo import AsyncMongoClient
from app.config.config import get_settings
from app.database.models.user import User


settings = get_settings()
mongo_client = None

async def init_db():
    global mongo_client
    db_connection_string = settings.DATABASE_URI

    if not db_connection_string:
        raise ValueError('DATABASE_URI is not set in environment variables')

    mongo_client = AsyncMongoClient(db_connection_string)
    await init_beanie(
        database=mongo_client.get_default_database(),
        document_models=[User]
    )