# api/services/dynamo.py

"""
DynamoDB service.

Provides a helper function to save metadata about uploaded media files to DynamoDB.
"""

import boto3
from datetime import datetime
from api.core.config import settings

# Shared DynamoDB resource (singleton, initialized once per process)
_dynamodb_resource = None


def get_dynamodb():
    """
    Lazily initializes and returns a shared DynamoDB resource.

    This function ensures that boto3 does not create a new
    resource client on every request, improving performance.

    Returns:
        boto3.resources.factory.dynamodb.ServiceResource: Shared DynamoDB resource.
    """
    global _dynamodb_resource
    if _dynamodb_resource is None:
        _dynamodb_resource = boto3.resource(
            "dynamodb",
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            aws_session_token=settings.AWS_SESSION_TOKEN,
        )
    return _dynamodb_resource


async def save_media_metadata(media_id: str, filename: str, s3_key: str, content_type: str, media_url: str):
    """
    Save metadata about an uploaded media file to DynamoDB.

    Args:
        media_id (str): Unique UUID identifying the media.
        filename (str): Original filename as uploaded by the user.
        s3_key (str): Object key under which the file is stored in S3.
        content_type (str): MIME type of the file (e.g., "image/png").
        media_url (str): Public or internal URL to access the uploaded media.

    Raises:
        Exception: Any boto3 error (e.g., access denied, table not found).
    """
    dynamodb = get_dynamodb()
    table = dynamodb.Table(settings.AWS_DYNAMODB_MEDIA_TABLE_NAME)
    uploaded_at = datetime.utcnow().isoformat()

    table.put_item(Item={
        "id": media_id,
        "filename": filename,
        "s3_key": s3_key,
        "content_type": content_type,
        "uploaded_at": uploaded_at,
        "url": media_url
    })
