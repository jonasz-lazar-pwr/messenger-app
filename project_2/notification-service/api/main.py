# api/main.py

from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.core.middleware import add_middleware
from api.routes import health, notification

# Define the startup and shutdown logic for the application
@asynccontextmanager
async def lifespan(_app: FastAPI):
    print("Starting up notification-service...")
    yield
    print("Shutting down notification-service...")

app = FastAPI(
    lifespan=lifespan,
    title="Notification Service API",
    description="Handles email notifications using SNS and stores notification history in DynamoDB.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Apply global middleware (CORS etc.)
add_middleware(app)

# Mount routers
app.include_router(health.router, prefix="/healthz")
app.include_router(notification.router, prefix="/api/notifications")