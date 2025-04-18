from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.core.config import settings

origins = settings.ALLOWED_ORIGINS.split(",")

def add_middleware(app: FastAPI):
    if settings.ALLOWED_ORIGINS.strip() == "*":
        allow_origins = ["*"]
        allow_credentials = False
    else:
        allow_origins = [origin.strip() for origin in settings.ALLOWED_ORIGINS.split(",")]
        allow_credentials = True

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_credentials=allow_credentials,
        allow_methods=["*"],
        allow_headers=["*"],
    )
