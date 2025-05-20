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
    echo=False,
    pool_pre_ping=True,      # Check if connections are alive before using them
    pool_size=5,             # Initial number of connections in the pool
    max_overflow=10,         # Max number of connections to create beyond the pool size
    pool_timeout=30,         # Max wait time for a connection from the pool
    pool_recycle=1800,       # Refresh the connection every 30 minutes
)

# Create an async session factory
async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)
