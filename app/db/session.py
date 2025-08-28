from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool
from app.core.config import settings
from typing import AsyncGenerator

async_engine = create_async_engine(
    str(settings.DATABASE_URL),
    pool_pre_ping=True,
    poolclass=NullPool,
    echo=False,
    future=True,
)

SessionLocal = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session