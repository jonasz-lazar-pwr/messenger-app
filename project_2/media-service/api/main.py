# api/main.py

"""
Main application entry point for the Media Service.

This module initializes the FastAPI app, sets up middleware,
and mounts all routes including health checks and media endpoints.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.core.middleware import add_middleware
from api.routes import media
from api.services.s3 import close_s3_client


@asynccontextmanager
async def lifespan(_app: FastAPI):
    print("Starting up media-service...")
    try:
        yield
    finally:
        print("Shutting down media-service...")
        await close_s3_client()


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

@app.get(
    "/healthz/",
    summary="Health check",
    description="Basic health check endpoint",
    tags=["Health"]
)
def health_check():
    return {"status": "ok"}

# Mount route modules under specified prefixes
app.include_router(media.router, prefix="/media")
