import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    ALLOWED_ORIGINS: str
    # AWS Cognito
    COGNITO_POOL_ID: str
    COGNITO_CLIENT_ID: str
    COGNITO_ISSUER_URL: str
    # AWS S3
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_SESSION_TOKEN: str
    AWS_REGION: str
    AWS_S3_BUCKET_NAME: str

    class Config:
        env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")

settings = Settings()
