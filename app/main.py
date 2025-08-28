import logging
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
from app.db.session import async_engine
from app.db.base import Base
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from app.api.routes.auth import router as auth_router
from app.api.routes.notes import router as notes_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.RUN_DB_MIGRATIONS_ON_STARTUP:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    try:
        yield
    finally:
        await async_engine.dispose()


app = FastAPI(
    title="Notes API",
    version="1.0.0",
    description="Простой сервис заметок с JWT-аутентификацией.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

log_level_name = getattr(settings, "LOG_LEVEL", "INFO")
log_level = getattr(logging, str(log_level_name).upper(), logging.INFO)
logging.getLogger().handlers.clear()
logging.basicConfig(
    level=log_level,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    stream=sys.stdout,
    force=True,
)

# >>> Подключаем роутеры
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(notes_router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema.setdefault("components", {}).setdefault("securitySchemes", {})[
        "bearerAuth"
    ] = {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    openapi_schema["security"] = [{"bearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.get("/", tags=["health"])
async def root():
    return {"status": "ok"}
