# === shared/db.py ===
"""
Synchronous Database Session Manager for AWS Lambda.

This module sets up a shared SQLAlchemy engine and session factory
for use across AWS Lambda handlers in a microservice architecture.

The connection uses the `psycopg2` driver to connect to a PostgreSQL database.
All database credentials are loaded from environment variables.

Environment Variables:
    PSQL_USER (str): PostgreSQL username.
    PSQL_PASSWORD (str): PostgreSQL password.
    PSQL_HOST (str): PostgreSQL host (hostname or IP address).
    PSQL_PORT (str): PostgreSQL port number.
    PSQL_NAME (str): PostgreSQL database name.

Example usage:
    with sync_session() as session:
        result = session.execute(select(...))
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# --- Environment Configuration ---
DB_USER = os.environ["PSQL_USER"]
DB_PASS = os.environ["PSQL_PASSWORD"]
DB_HOST = os.environ["PSQL_HOST"]
DB_PORT = os.environ["PSQL_PORT"]
DB_NAME = os.environ["PSQL_NAME"]

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# --- Synchronous Engine and Session Factory ---
engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
)

sync_session = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)
