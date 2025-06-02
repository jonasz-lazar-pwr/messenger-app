# === services/dynamo.py ===

"""DynamoDB service for persisting notification metadata.

Provides a shared DynamoDB client and a helper function to save
notification records in a specified DynamoDB table.
"""

import os
import boto3

# Shared DynamoDB resource (singleton)
_dynamodb_resource = None


def get_dynamodb():
    """Lazily initialize and return a shared DynamoDB resource.

    Returns:
        boto3.resources.factory.dynamodb.ServiceResource: A shared DynamoDB resource object.
    """
    global _dynamodb_resource
    if _dynamodb_resource is None:
        _dynamodb_resource = boto3.resource(
            "dynamodb",
            region_name=os.environ["AWS_REGION"],
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
            aws_session_token=os.environ["AWS_SESSION_TOKEN"],
        )
    return _dynamodb_resource


def save_notification(notification_id: str, user_email: str, message: str, sent_at: str):
    """Save a notification record to DynamoDB.

    Args:
        notification_id (str): Unique UUID for the notification.
        user_email (str): Email address of the recipient.
        message (str): Content of the notification message.
        sent_at (str): ISO 8601 UTC timestamp of when the notification was sent.
    """
    dynamodb = get_dynamodb()
    table = dynamodb.Table(os.environ["AWS_DYNAMODB_NOTIFICATION_TABLE_NAME"])

    item = {
        "notification_id": notification_id,
        "user_email": user_email,
        "message": message,
        "sent_at": sent_at,
    }

    table.put_item(Item=item)
