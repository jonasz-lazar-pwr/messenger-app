# === services/sns.py ===

"""SNS service for publishing notifications.

Provides utility functions to initialize an SNS client and publish
messages to a configured SNS topic.

Environment Variables:
    - AWS_REGION
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY
    - AWS_SESSION_TOKEN
    - AWS_SNS_TOPIC_ARN
"""

import os
import boto3

_sns_client = None


def get_sns_client():
    """Initialize and return a shared SNS client instance.

    Returns:
        boto3.client: A configured SNS client.

    Raises:
        Exception: If the client cannot be initialized.
    """
    global _sns_client

    if _sns_client is not None:
        return _sns_client

    _sns_client = boto3.client(
        "sns",
        region_name=os.environ["AWS_REGION"],
        aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
        aws_session_token=os.environ["AWS_SESSION_TOKEN"],
    )
    return _sns_client


def send_notification_to_sns(user_email: str, message: str) -> dict:
    """Publish a notification message to the configured SNS topic.

    Args:
        user_email (str): Recipient email address (for context only).
        message (str): Notification message body.

    Returns:
        dict: Response from SNS publish operation.

    Raises:
        Exception: If the message fails to publish.
    """
    sns = get_sns_client()

    response = sns.publish(
        TopicArn=os.environ["AWS_SNS_TOPIC_ARN"],
        Message=message,
        Subject=f"New notification for {user_email}",
    )
    return response
