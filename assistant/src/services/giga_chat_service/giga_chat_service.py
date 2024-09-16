from enum import Enum
import backoff
from langchain.agents import AgentExecutor, create_gigachat_functions_agent
from langchain_community.chat_models.gigachat import GigaChat
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.runnables import Runnable
import orjson

from src.utils.cache import get_redis
from src.core.config import settings
from src.core.logger import assistant_logger
from src.services.giga_chat_service.main_functions import tools

giga_chat: GigaChat | None = None


async def get_giga_chat() -> GigaChat:
    return giga_chat


class MessageTypes(Enum):
    human_message = HumanMessage
    ai_message = AIMessage


class ChatHistoryService:
    def __init__(self, cache, user_id) -> None:
        self.user_id = user_id
        self.cache = cache
        self.chat_history_from_cache = list()

    def get_history(self) -> list | None:
        self.chat_history_from_cache: list[dict] = orjson.loads(
            self.cache.get("user_" + self.user_id) or "[]"
        )
        chat_history = list()
        for entry in self.chat_history_from_cache:
            for message_type in MessageTypes:
                if entry.get(message_type.name):
                    chat_history.append(
                        message_type.value(content=entry.get(message_type.name))
                    )

        return chat_history

    def add_entry(self, message_type, content) -> None:
        self.chat_history_from_cache.append({message_type: content})

    def save(self) -> None:
        self.cache.set(
            "user_" + self.user_id,
            orjson.dumps(self.chat_history_from_cache),
            ex=settings.chat_expire_in_seconds,
        )


class GigaChatService:
    """Сервис взаимодействующий с GigaChat."""

    def __init__(self):
        self.tools = tools
        self.cache = get_redis()

    async def main_giga_chat(self, user_input: str, user_id: str | None = None) -> str:
        """Создание и зупуск агента GigaChat."""

        agent = await self.create_giga_chat_agent()
        chat_history_service = ChatHistoryService(cache=self.cache, user_id=user_id)
        return await self.run_agent(
            agent, user_input, chat_history_service=chat_history_service
        )

    @backoff.on_exception(
        backoff.expo,
        ConnectionError,
        max_tries=3,
    )
    async def create_giga_chat_agent(self) -> Runnable:
        """Создание агента GigaChat."""

        giga_chat = GigaChat(
            credentials=settings.auth_data,
            scope=settings.giga_chat_scope,
            model=settings.giga_chat_model,
            verify_ssl_certs=False,
        )

        return create_gigachat_functions_agent(giga_chat, self.tools)

    async def run_agent(
        self,
        agent: Runnable,
        user_input: str,
        system_message: str | None = None,
        chat_history_service: ChatHistoryService | None = None,
    ) -> str:
        """Запуск агента GigaChat."""

        agent_executor = AgentExecutor(
            agent=agent, tools=self.tools, verbose=True, system_message=system_message
        )

        chat_history = chat_history_service.get_history()

        reply = agent_executor.invoke(
            {
                "chat_history": chat_history,
                "input": user_input,
            }
        )["output"]

        chat_history_service.add_entry(
            message_type=MessageTypes.human_message.name, content=user_input
        )
        chat_history_service.add_entry(
            message_type=MessageTypes.ai_message.name, content=reply
        )

        chat_history_service.save()

        assistant_logger.info(reply)

        return reply
