# api/services/dynamo.py

"""
DynamoDB service.

Provides a globally shared DynamoDB resource and helper function
to persist notification metadata in DynamoDB.
"""

import boto3
from api.core.config import settings

# Shared DynamoDB resource (singleton)
_dynamodb_resource = None


def get_dynamodb():
    """
    Lazily initializes and returns a shared DynamoDB resource.

    This function avoids repeated creation of boto3 DynamoDB clients.

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


async def save_notification(notification_id: str, user_email: str, message: str, sent_at: str):
    """
    Save a notification record to the DynamoDB Notifications table.

    Args:
        notification_id (str): UUID string identifying the notification.
        user_email (str): Email address of the notification recipient.
        message (str): Message content of the notification.
        sent_at (str): ISO 8601 UTC timestamp of when the notification was sent.

    Raises:
        Exception: Any boto3 error encountered during the write operation.
    """
    dynamodb = get_dynamodb()
    table = dynamodb.Table(settings.AWS_DYNAMODB_NOTIFICATION_TABLE_NAME)

    item = {
        "notification_id": notification_id,
        "user_email": user_email,
        "message": message,
        "sent_at": sent_at
    }

    table.put_item(Item=item)
