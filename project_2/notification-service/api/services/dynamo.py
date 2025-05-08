# api/services/dynamo.py

"""
DynamoDB service module for storing notifications.

This module provides functionality to persist notification metadata in a DynamoDB table.
"""

import boto3
from api.core.config import settings

# Initialize the DynamoDB resource with proper credentials and endpoint (AWS or LocalStack)
dynamo = boto3.resource(
    "dynamodb",
    endpoint_url=settings.DYNAMODB_ENDPOINT,
    region_name=settings.AWS_REGION,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    aws_session_token=settings.AWS_SESSION_TOKEN
)

# Reference to the DynamoDB table where notifications are stored
table = dynamo.Table(settings.DYNAMODB_NOTIFICATION_TABLE_NAME)


async def save_notification(notification_id: str, user_email: str, message: str, sent_at: str):
    """
    Saves the notification metadata to the DynamoDB Notifications table.

    This function persists the notification record, including the unique ID,
    recipient email, message content, and timestamp, into DynamoDB.

    Args:
        notification_id (str): Unique identifier for the notification (UUID4 string).
        user_email (str): The email address of the recipient.
        message (str): The notification message content.
        sent_at (str): ISO 8601 formatted UTC timestamp representing when the notification was sent.

    Returns:
        None

    Raises:
        boto3.exceptions.Boto3Error: If an error occurs while writing to DynamoDB.
    """
    item = {
        "notification_id": notification_id,
        "user_email": user_email,
        "message": message,
        "sent_at": sent_at
    }
    table.put_item(Item=item)
