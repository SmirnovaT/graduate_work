from fastapi import APIRouter, Depends

from src.schemas.assistant import (
    ProviderRequest,
    YandexResponseBody,
    VKResponseBody
)
from src.services.assistant_service import (
    AssistantService,
    get_assistant_service
)

router = APIRouter(tags=["assistant"])


@router.post(
    "/vk",
    summary="Обработчик запросов от Голосового ассистента Маруси",
)
async def vk_webhook(
    request: ProviderRequest,
    assistant_service: AssistantService = Depends(get_assistant_service),
) -> VKResponseBody:
    user_id = request.session.get("user").get("user_id")
    owner_id = request.session.get("user_id")
    command = request.request.get("command")
    session_id = request.session.get("session_id")
    message_id = request.session.get("message_id")
    

    giga_response = await assistant_service.response(command, user_id)

    return VKResponseBody(
        response={
            "text": giga_response,
            "end_session": False,
        },
        session={
            "session_id": session_id,
            "user_id": owner_id,
            "message_id": message_id,
        },
        version="1.0",
    )

@router.post(
    "/yandex",
    summary="Обработчик запросов от Голосового ассистента Алисы",
)
async def yandex_webhook(
    request: ProviderRequest,
    assistant_service: AssistantService = Depends(get_assistant_service),
) -> YandexResponseBody:
    user_id = request.session.get("user").get("user_id")
    command = request.request.get("command")

    giga_response = await assistant_service.response(command, user_id)

    return YandexResponseBody(
        response={
            "text": giga_response,
            "end_session": False,
        },
        version="1.0",
    )
