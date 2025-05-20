# api/main.py

"""
Main entry point for the Chat Service API.

This module initializes the FastAPI application, sets up middleware,
mounts all the routers, and defines lifecycle events.

Mounted routers:
- /healthz: Health check endpoint.
- /api/messages: Message-related endpoints (create, get messages).
- /api/chats: Chat-related endpoints (list chats).
- /api/users: User-related endpoints (search, register).

The service handles user-to-user chat functionality, including messages,
file attachments (via the media service), and user discovery.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.core.middleware import add_middleware
from api.routes import message, chat, user


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    Define the startup and shutdown logic for the chat-service.

    Args:
        _app (FastAPI): The FastAPI application instance.

    Yields:
        None
    """
    print("Starting up chat-service...")
    yield
    print("Shutting down chat-service...")


# Initialize the FastAPI application
app = FastAPI(
    lifespan=lifespan,
    title="Chat Service API",
    description="Handles user-to-user chats and messages",
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

# Mount routers for different parts of the API
app.include_router(message.router, prefix="/messages")
app.include_router(chat.router, prefix="/chats")
app.include_router(user.router, prefix="/users")