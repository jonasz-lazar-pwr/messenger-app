# api/db/session.py

"""
Database session factory.

This module sets up the SQLAlchemy asynchronous engine and session
maker using configuration from environment variables. It provides
the `async_session` factory to create async DB sessions.

Usage:
    from .session import async_session
"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from api.core.config import settings

# Build the database URL from environment settings
DATABASE_URL = (
    f"postgresql+asyncpg://{settings.PSQL_USER}:{settings.PSQL_PASSWORD}"
    f"@{settings.PSQL_HOST}:{settings.PSQL_PORT}/{settings.PSQL_NAME}"
)

# Create an async SQLAlchemy engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,           # Logs SQL statements for debugging
    pool_pre_ping=True,  # Checks if connections are alive
)

# Create an async session factory
async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)
