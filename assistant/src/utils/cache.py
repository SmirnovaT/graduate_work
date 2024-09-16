from abc import ABC, abstractmethod
from typing import Any

import orjson
from redis import Redis

from src.core.config import settings
from src.core.logger import assistant_logger

redis_instance = Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    username="",
    password="",
)


def get_redis() -> Redis:
    return redis_instance


class BaseCacheService(ABC):
    @abstractmethod
    def get(self, key: str) -> Any:
        pass

    @abstractmethod
    def set(self, key: str, value: dict) -> None:
        pass

    @abstractmethod
    def cached(self, func: callable) -> callable:
        pass


class RedisCacheService(BaseCacheService):
    """Имплементация класса для кеширования данных"""

    def __init__(self, cache: Redis):
        self.cache = cache

    def get(self, key: str) -> Any:
        """Получение данных из кеша по ключу"""

        try:
            data = self.cache.get(key)
        except Exception as exc:
            assistant_logger.error(
                f"Ошибка при взятии значения по ключу {key} из кеша: {exc}"
            )
            return None

        if not data:
            return None

        return orjson.loads(data)

    def set(self, key: str, value: dict) -> None:
        """Сохранение единичной записи в кеш"""

        try:
            self.cache.set(
                key, orjson.dumps(value), ex=settings.cache_expire_in_seconds
            )
        except Exception as exc:
            assistant_logger.error(f"Error: cannot write value for key '{key}' in cache: {exc}")

    def cached(self, func):
        """Декоратор для кеширования незакешированных данных, ключ - UUID единицы данных"""

        def wrapper(id_: str):
            value = self.get(id_)
            if not value:
                value = func(id_)
                self.set(key=id_, value=value)
            return value

        return wrapper
