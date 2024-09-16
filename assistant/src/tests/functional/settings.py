from dotenv import load_dotenv
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Конфигурация тестов"""

    api_vk: str = "http://127.0.0.1:8001/api/v1/assistant/vk"
    api_yandex: str = "http://127.0.0.1:8001/api/v1/assistant/yandex"


def get_settings():
    load_dotenv()
    return Settings()


test_settings = get_settings()
