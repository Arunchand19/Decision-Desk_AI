from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    gemini_api_key: str | None = None
    jwt_secret: str = "change-me-in-production"
    database_url: str = "sqlite:///./support_ai.db"
    api_url: str = "http://localhost:8000"
    top_k: int = 3
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 60

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
