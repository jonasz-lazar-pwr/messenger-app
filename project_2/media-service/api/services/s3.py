# api/services/s3.py

"""
S3 service.

Provides the logic to upload files to S3-compatible storage and return metadata for the uploaded file.
"""

from typing import Tuple
import aioboto3
import uuid
from api.core.config import settings


async def upload_file_to_s3(file, filename: str, content_type: str) -> Tuple[str, str, str]:
    """
    Upload a file to S3-compatible storage (e.g., AWS S3 or LocalStack).

    This function:
    - Generates a unique media ID (UUID).
    - Constructs the S3 object key based on the original filename.
    - Uploads the file asynchronously using aioboto3.
    - Returns the media ID, the S3 key (path), and a full URL for accessing the file.

    Args:
        file: The incoming FastAPI UploadFile object (already opened).
        filename (str): The original name of the file (used in the key).
        content_type (str): MIME type of the file (e.g., "image/jpeg", "image/png").

    Returns:
        Tuple[str, str, str]:
            - media_id: UUID string identifying the media.
            - s3_key: Path/key where the file is stored in S3.
            - media_url: Full URL (public or internal) to access the uploaded file.

    Raises:
        Any exceptions from aioboto3 will propagate to the caller.
    """
    # Generate a unique UUID for the media
    media_id = str(uuid.uuid4())

    # Define the S3 key (object path inside the bucket)
    s3_key = filename  # Optionally could use f"{media_id}_{filename}" for uniqueness

    # Create an aioboto3 session and upload the file asynchronously
    session = aioboto3.Session()
    async with session.client(
        "s3",
        region_name=settings.AWS_REGION,
        endpoint_url=settings.S3_ENDPOINT,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        aws_session_token=settings.AWS_SESSION_TOKEN,
    ) as s3:
        await s3.upload_fileobj(
            file.file,  # File-like object
            settings.S3_BUCKET_NAME,
            s3_key,
            ExtraArgs={"ContentType": content_type}  # Set proper MIME type metadata
        )

    # Build the full media URL (may be public or internal depending on your setup)
    media_url = f"{settings.S3_ENDPOINT}/{settings.S3_BUCKET_NAME}/{s3_key}"

    return media_id, s3_key, media_url
