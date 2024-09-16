from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Конфигурация проекта"""

    project_name: str

    cors_origins: list[str] = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = ["*"]
    cors_allow_headers: list[str] = ["*"]

    redis_host: str = "127.0.0.1"
    redis_port: int = 6379
    redis_user: str = "app"
    redis_password: str

    cache_expire_in_seconds: int = 300
    chat_expire_in_seconds: int = 120

    client_secret: str
    auth_data: str
    giga_chat_model: str = "GigaChat"
    giga_chat_scope: str = "GIGACHAT_API_PERS"

    api_films: str = "http://127.0.0.1:8000/api/v1/films"
    api_persons: str = "http://127.0.0.1:8000/api/v1/persons"

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent.parent / ".env"
    )


@lru_cache
def get_settings():
    load_dotenv()
    return Settings()


settings = get_settings()
