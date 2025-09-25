from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    DATABASE_URI: str
    CLOUD_NAME: str
    API_KEY: str
    API_SECRET: str
    GEMINI_API_KEY: str
    JWT_SECRET_KEY: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()
