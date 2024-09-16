from functools import lru_cache
from urllib.parse import urlencode

import httpx
from fastapi import Depends
from langchain_community.chat_models.gigachat import GigaChat

from src.core.config import settings
from src.core.logger import assistant_logger

from src.services.giga_chat_service.giga_chat_service import (
    GigaChatService,
    get_giga_chat,
)


class AssistantService:
    """Сервис взаимодействующий с голосовым ассистентом."""

    def __init__(self) -> None:
        self.giga_chat = GigaChatService()

    async def response(self, command: str, user_id: str) -> str:
        """Обработчик сообщения от голосового ассистента."""

        try:
            response = await self.giga_chat.main_giga_chat(command, user_id)
            assistant_logger.info("GigaChat: got a reply")

        except Exception as e:
            assistant_logger.error(f"Gigachat: cannot get a reply, {e}")
            response = await self.standard_response()

        return response

    @staticmethod
    async def standard_response() -> str:
        """Если не удалось получить ответ от Gigachat,
        сервис возвращает 10 фильмов с самым высоким рейтингом."""

        params = {"sort": "-imdb_rating", "page_size": 10, "page_number": 1}
        full_url = f"{settings.api_films}/?{urlencode(params)}"

        try:
            films_data = httpx.get(full_url)
        except Exception as e:
            assistant_logger.info(f"movies service: unreacahble, {e}")
            return "К сожалению, сервис сейчас недоступен"

        best_films = [film["title"] for film in films_data.json()]

        return f"""К сожалению, поиск сейчас не работает, 
        могу вам рассказать о фильмах с самым высоким рейтингом: {best_films}"""


@lru_cache()
def get_assistant_service(
    _: GigaChat = Depends(get_giga_chat),
) -> AssistantService:
    return AssistantService()
