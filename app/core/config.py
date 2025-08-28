from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyUrl
from typing import List


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


    SECRET_KEY: str = "change-me"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    ALGORITHM: str = "HS256"

    RUN_DB_MIGRATIONS_ON_STARTUP: bool = True

    # Runtime DB URL (используется приложением)
    DATABASE_URL: AnyUrl = "postgresql+asyncpg://postgres:postgres@db:5432/notes"

    # CORS
    CORS_ALLOW_ORIGINS: List[str] = ["*"]


    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_DB: Optional[str] = None

    TEST_DATABASE_URL: Optional[str] = None


settings = Settings()
