# api/main.py

"""
Notification Service main application.

Initializes the FastAPI app, applies middleware, and mounts routes
for health checks and notification handling.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.core.middleware import add_middleware
from api.routes import health, notification


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Define startup and shutdown logic for the notification service."""
    print("Starting up notification-service...")
    yield
    print("Shutting down notification-service...")


# Initialize the FastAPI application
app = FastAPI(
    lifespan=lifespan,
    title="Notification Service API",
    description="Handles email notifications using SNS and stores notification history in DynamoDB.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Apply global middleware (e.g., CORS)
add_middleware(app)

# Mount routers for different parts of the API
app.include_router(health.router, prefix="/healthz")
app.include_router(notification.router, prefix="/notifications")