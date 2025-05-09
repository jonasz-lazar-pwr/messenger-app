# api/main.py

"""
Main application entry point for the Media Service.

This module initializes the FastAPI app, sets up middleware,
and mounts all routes including health checks and media endpoints.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.core.middleware import add_middleware
from api.routes import health, media


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    Define startup and shutdown logic for the application.

    Args:
        _app (FastAPI): The FastAPI app instance.

    Yields:
        None: Used to manage application lifespan events.
    """
    print("Starting up media-service...")
    yield
    print("Shutting down media-service...")


# Initialize FastAPI app with metadata and custom lifespan management
app = FastAPI(
    lifespan=lifespan,
    title="Media Service API",
    description="Handles media uploads and stores metadata in the DB.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Apply global middleware (e.g., CORS)
add_middleware(app)

# Mount route modules under specified prefixes
app.include_router(health.router, prefix="/healthz")
app.include_router(media.router, prefix="/media")