# api/services/sns.py

import boto3
from api.core.config import settings

sns_client = boto3.client(
    "sns",
    endpoint_url=settings.SNS_ENDPOINT,
    region_name=settings.AWS_REGION,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    aws_session_token=settings.AWS_SESSION_TOKEN
)

def send_notification_to_sns(user_email: str, message: str) -> dict:
    """
    Publishes a message to the SNS topic for email notifications.

    Args:
        user_email (str): The email of the user (used in the Subject line).
        message (str): The message content to send.

    Returns:
        dict: The SNS publish response metadata.
    """
    response = sns_client.publish(
        TopicArn=settings.SNS_TOPIC_ARN,
        Message=message,
        Subject=f"New notification for {user_email}"
    )
    return response