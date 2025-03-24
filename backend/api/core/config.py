import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    COGNITO_POOL_ID: str
    COGNITO_CLIENT_ID: str
    ALLOWED_ORIGINS: str
    COGNITO_ISSUER_URL: str

    class Config:
        env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")

settings = Settings()
