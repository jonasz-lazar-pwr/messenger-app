# api/services/dynamo.py

"""
DynamoDB service.

Provides a helper function to save metadata about uploaded media files to DynamoDB.
"""

import boto3
from datetime import datetime
from api.core.config import settings


async def save_media_metadata(media_id: str, filename: str, s3_key: str, content_type: str, media_url: str):
    """
    Save media metadata to DynamoDB.

    This function:
    - Connects to the configured DynamoDB table.
    - Prepares a metadata item with details about the uploaded media.
    - Inserts the item into DynamoDB.

    Args:
        media_id (str): UUID string identifying the media.
        filename (str): The original filename of the uploaded file.
        s3_key (str): The S3 object key/path where the file is stored.
        content_type (str): MIME type of the file (e.g., "image/jpeg").
        media_url (str): Full URL where the media can be accessed.

    Raises:
        Exception: Any exception from boto3 (e.g., connection or permission errors) will propagate.
    """
    # Initialize DynamoDB resource
    dynamodb = boto3.resource(
        "dynamodb",
        region_name=settings.AWS_REGION,
        endpoint_url=settings.DYNAMODB_ENDPOINT,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        aws_session_token=settings.AWS_SESSION_TOKEN,
    )

    # Get the target table
    table = dynamodb.Table(settings.DYNAMODB_TABLE_NAME)

    # Timestamp when the upload occurred (ISO format)
    uploaded_at = datetime.utcnow().isoformat()

    # Put the metadata item into DynamoDB
    table.put_item(Item={
        "id": media_id,
        "filename": filename,
        "s3_key": s3_key,
        "content_type": content_type,
        "uploaded_at": uploaded_at,
        "url": media_url
    })