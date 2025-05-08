# api/services/sns.py

"""
SNS service module for publishing notifications.

Provides functionality to send messages to the configured SNS topic for email-based notifications.
"""

import boto3
from api.core.config import settings

# Initialize the SNS client with appropriate credentials and endpoint (AWS or LocalStack)
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
    Publishes a notification message to the SNS topic.

    This function sends an email-based notification via the configured SNS topic.
    The email subject includes the recipient's email, and the message body contains the actual content.

    Args:
        user_email (str): The recipient's email address (used in the subject line).
        message (str): The content of the notification message.

    Returns:
        dict: Response metadata from the SNS publish action (includes MessageId, ResponseMetadata, etc.).

    Raises:
        botocore.exceptions.BotoCoreError: If the SNS client encounters an error during publishing.
    """
    response = sns_client.publish(
        TopicArn=settings.SNS_TOPIC_ARN,
        Message=message,
        Subject=f"New notification for {user_email}"
    )
    return response