# api/routes/notification.py

"""
Notification routes for sending notifications.

Exposes endpoints to handle notification publishing and metadata storage.
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
from uuid import uuid4
from api.schemas.notification import SendNotificationIn, NotificationOut
from api.services.sns import send_notification_to_sns
from api.services.dynamo import save_notification

# Create a router instance for notification-related routes
router = APIRouter()


@router.post(
    "/send",
    response_model=NotificationOut,
    summary="Send a notification",
    description=(
        "Publishes a notification to the SNS topic (email notification) and saves the record "
        "to the DynamoDB Notifications table. "
        "Returns the full notification metadata including ID and timestamp."
    )
)
async def send_notification(payload: SendNotificationIn):
    """
    Send a notification to a user via email and store the notification metadata in DynamoDB.

    Process:
    - Generates a unique notification ID (UUID4) and captures the current UTC timestamp.
    - Publishes the notification message to the SNS topic.
    - Saves the notification metadata (ID, email, message, timestamp) to the DynamoDB table.

    Args:
        payload (SendNotificationIn): The input payload containing `user_email` and `message`.

    Returns:
        NotificationOut: Full metadata of the sent notification (notification_id, user_email, message, sent_at).

    Raises:
        HTTPException:
            - 500 Internal Server Error if sending the notification fails.
            - 500 Internal Server Error if saving the metadata to DynamoDB fails.
    """
    # Generate a unique notification ID and timestamp
    notification_id = str(uuid4())
    sent_at = datetime.utcnow().isoformat()

    # Attempt to send the notification via SNS
    try:
        sns_response = send_notification_to_sns(str(payload.user_email), payload.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send notification: {str(e)}")

    # Attempt to save the notification metadata to DynamoDB
    try:
        await save_notification(notification_id, str(payload.user_email), payload.message, sent_at)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save notification: {str(e)}")

    # Return the full notification metadata
    return NotificationOut(
        notification_id=notification_id,
        user_email=payload.user_email,
        message=payload.message,
        sent_at=datetime.fromisoformat(sent_at)
    )