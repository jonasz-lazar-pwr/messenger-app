# === shared/sqs.py ===
"""
SQS integration utilities for publishing notification messages.

This module initializes the SQS client and exposes a function to
send notification messages (as JSON) to the designated SQS queue.

Required environment variables:
    - AWS_REGION
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY
    - AWS_SESSION_TOKEN
    - AWS_SQS_NOTIFICATION_QUEUE_URL
    - NOTIFICATION_RECEIVER_EMAIL
"""

import os
import json
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from sqlalchemy import select
from sqlalchemy.orm import Session as SyncSession
from shared.models import User

# Initialize the SQS client using credentials from environment variables
sqs = boto3.client(
    "sqs",
    region_name=os.environ["AWS_REGION"],
    aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    aws_session_token=os.environ["AWS_SESSION_TOKEN"],
)

QUEUE_URL = os.environ.get("AWS_SQS_NOTIFICATION_QUEUE_URL")


def send_notification_to_sqs(user_email: str, message: str) -> None:
    """
    Publish a notification message to Amazon SQS.

    The message payload includes the recipient email and the message content,
    serialized as JSON and sent to the queue defined by `AWS_SQS_NOTIFICATION_QUEUE_URL`.

    Args:
        user_email: Recipient's email address.
        message: Notification message content.

    Raises:
        RuntimeError: If QUEUE_URL is not defined or if sending fails.
    """
    if not QUEUE_URL:
        raise RuntimeError("SQS queue URL is not configured")

    payload = {
        "user_email": user_email,
        "message": message,
    }

    try:
        sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps(payload)
        )
    except (BotoCoreError, ClientError) as exc:
        raise RuntimeError("Failed to send message to SQS") from exc


def notify_about_message(
    db: SyncSession,
    sender_sub: str,
    message_text: str | None,
    has_media: bool,
) -> None:
    """
    Construct and send a notification to SQS for a new message event.

    Args:
        db: Open SQLAlchemy session.
        sender_sub: Cognito sub of the sender.
        message_text: The plain text message, if any.
        has_media: Whether the message contains media.

    Raises:
        RuntimeError: If recipient email is missing in environment.
    """
    result = db.execute(select(User).where(User.sub == sender_sub))
    sender = result.scalar_one_or_none()
    sender_name = (
        f"{sender.first_name} {sender.last_name}"
        if sender else f"Unknown ({sender_sub})"
    )

    notification_message = (
        f"You have received a new message\n\n"
        f"From: {sender_name}\n"
        f"Message: {message_text or '[Media file only]'}\n"
        f"Contains media: {'Yes' if has_media else 'No'}"
    )

    receiver_email = os.environ.get("NOTIFICATION_RECEIVER_EMAIL")
    if not receiver_email:
        raise RuntimeError("Missing NOTIFICATION_RECEIVER_EMAIL in environment")

    send_notification_to_sqs(
        user_email=receiver_email,
        message=notification_message
    )
