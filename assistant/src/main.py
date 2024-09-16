from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.utils.cache import get_redis
from src.api.v1 import assistant
from src.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_instance = get_redis()
    yield
    redis_instance.close()


app = FastAPI(
    version="1.0.0",
    title=settings.project_name,
    summary="Voice assistant",
    description="Entry point for clients to voice search for cinema content",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
    contact={
        "name": "Amazing python team",
        "email": "amazaingpythonteam@fake.com",
    },
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)

app.include_router(assistant.router, prefix="/api/v1/assistant")

if __name__ == "__main__":
    # Запуск приложения для целей отладки, параметры удобнее держать в коде
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
    )
