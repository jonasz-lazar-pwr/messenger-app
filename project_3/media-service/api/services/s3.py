# api/services/s3.py

"""
S3 service.

Provides the logic to upload files to S3-compatible storage and return metadata for the uploaded file.
"""

from typing import Tuple, Optional
import aioboto3
import uuid
from api.core.config import settings
from botocore.client import BaseClient

# Global session and shared client (initialized once)
_s3_session = aioboto3.Session()
_s3_client: Optional[BaseClient] = None  # Will be initialized on first use


async def get_s3_client():
    """
    Lazily initializes and returns a shared S3 client using aioboto3.

    Returns:
        aioboto3.client: The S3 client instance.
    """
    global _s3_client
    if _s3_client is None:
        _s3_client = await _s3_session.client(
            "s3",
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            aws_session_token=settings.AWS_SESSION_TOKEN,
        ).__aenter__()  # manually enter async context once
    return _s3_client


async def close_s3_client() -> None:
    global _s3_client
    if _s3_client is not None:
        # Call __aexit__ properly with correct types
        await _s3_client.__aexit__(None, None, None)
        _s3_client = None


async def upload_file_to_s3(file, filename: str, content_type: str) -> Tuple[str, str, str]:
    """
    Upload a file to S3-compatible storage (e.g., AWS S3).

    This function:
    - Generates a unique media ID (UUID).
    - Constructs the S3 object key based on the original filename.
    - Uploads the file using a shared S3 client.
    - Returns the media ID, the S3 key (path), and a full URL for accessing the file.

    Args:
        file: The incoming FastAPI UploadFile object (already opened).
        filename (str): The original name of the file (used in the key).
        content_type (str): MIME type of the file (e.g., "image/jpeg").

    Returns:
        Tuple[str, str, str]:
            - media_id: UUID string identifying the media.
            - s3_key: Path/key where the file is stored in S3.
            - media_url: Full URL to access the uploaded file.
    """
    # Generate a unique UUID for the media
    media_id = str(uuid.uuid4())
    # Define the S3 key (object path inside the bucket)
    s3_key = filename

    s3 = await get_s3_client()
    await s3.upload_fileobj(
        file.file,
        settings.AWS_S3_BUCKET_NAME,
        s3_key,
        ExtraArgs={"ContentType": content_type}
    )

    # Build the full media URL
    media_url = f"https://{settings.AWS_S3_BUCKET_NAME}.s3.{settings.AWS_REGION}.amazonaws.com/{s3_key}"
    return media_id, s3_key, media_url
