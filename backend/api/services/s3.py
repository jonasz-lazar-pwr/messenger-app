import boto3
from api.core.config import settings

s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    aws_session_token=settings.AWS_SESSION_TOKEN,
    region_name=settings.AWS_REGION
)

def upload_file_to_s3(file_obj, filename: str) -> str:
    s3_client.upload_fileobj(
        file_obj,
        settings.AWS_S3_BUCKET_NAME,
        filename
    )
    return f"https://{settings.AWS_S3_BUCKET_NAME}.s3.{settings.AWS_REGION}.amazonaws.com/{filename}"