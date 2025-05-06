# api/db/session.py

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from api.core.config import settings

DATABASE_URL = (
    f"postgresql+asyncpg://{settings.PSQL_USER}:{settings.PSQL_PASSWORD}"
    f"@{settings.PSQL_HOST}:{settings.PSQL_PORT}/{settings.PSQL_NAME}"
)

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
)

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)
