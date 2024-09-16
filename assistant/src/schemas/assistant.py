from typing import Any

from pydantic import BaseModel


class ProviderRequest(BaseModel):
    meta: dict[str, Any]
    request: dict[str, Any]
    session: dict[str, Any]
    version: str


class VKResponseBody(BaseModel):
    response: dict[str, Any]
    session: dict[str, Any]
    version: str


class YandexResponseBody(BaseModel):
    response: dict[str, Any]
    version: str
