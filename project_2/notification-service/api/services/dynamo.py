# api/services/dynamo.py

import boto3
from api.core.config import settings

dynamo = boto3.resource(
    "dynamodb",
    endpoint_url=settings.DYNAMODB_ENDPOINT,
    region_name=settings.AWS_REGION,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    aws_session_token=settings.AWS_SESSION_TOKEN
)

table = dynamo.Table(settings.DYNAMODB_NOTIFICATION_TABLE_NAME)

async def save_notification(notification_id: str, user_email: str, message: str, sent_at: str):
    """
    Saves the notification details to DynamoDB.

    Args:
        notification_id (str): Unique identifier for the notification (UUID4).
        user_email (str): The email of the recipient user.
        message (str): The message content.
        sent_at (str): ISO-formatted UTC timestamp of when the notification was sent.

    Returns:
        None
    """
    item = {
        "notification_id": notification_id,
        "user_email": user_email,
        "message": message,
        "sent_at": sent_at
    }
    table.put_item(Item=item)