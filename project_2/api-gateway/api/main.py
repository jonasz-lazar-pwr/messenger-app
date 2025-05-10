# api/main.py

from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.core.middleware import add_middleware
from api.routes import proxy, health


@asynccontextmanager
async def lifespan(_app: FastAPI):
    print("Starting up API Gateway...")
    yield
    print("Shutting down API Gateway...")

app = FastAPI(
    lifespan=lifespan,
    title="API Gateway",
    description="API Gateway for forwarding requests to chat, media, and notification services.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Apply global middleware (e.g., CORS)
add_middleware(app)

# Mount routers
app.include_router(health.router, prefix="/healthz")
app.include_router(proxy.router, prefix="/api")