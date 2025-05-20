# api/services/sns.py

"""
SNS service.

Provides a lazily initialized SNS client and function to send notifications
to the configured AWS SNS topic.
"""

import boto3
from api.core.config import settings

# Shared SNS client (lazy singleton)
_sns_client = None


def get_sns_client():
    """
    Lazily initializes and returns the shared SNS client.

    Returns:
        botocore.client.SNS: Boto3 SNS client
    """
    global _sns_client
    if _sns_client is None:
        _sns_client = boto3.client(
            "sns",
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            aws_session_token=settings.AWS_SESSION_TOKEN,
        )
    return _sns_client


def send_notification_to_sns(user_email: str, message: str) -> dict:
    """
    Publishes a notification message to the SNS topic.

    Args:
        user_email (str): Recipient's email (used in the subject).
        message (str): The notification body.

    Returns:
        dict: AWS SNS publish response.
    """
    sns = get_sns_client()
    return sns.publish(
        TopicArn=settings.AWS_SNS_TOPIC_ARN,
        Message=message,
        Subject=f"New notification for {user_email}"
    )
