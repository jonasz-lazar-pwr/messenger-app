# api/routes/notification.py

from fastapi import APIRouter, HTTPException
from datetime import datetime
from uuid import uuid4
from api.schemas.notification_item import SendNotificationIn, NotificationOut
from api.services.sns import send_notification_to_sns
from api.services.dynamo import save_notification

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
    Send a notification to a user via email and store the notification in DynamoDB.

    Workflow:
    1. Generate a unique `notification_id` (UUID4) and current UTC timestamp.
    2. Publish the notification message to the SNS topic (email-based notification).
    3. Save the notification details to the DynamoDB table (`Notifications`).

    Args:
        payload (SendNotificationIn): The notification input payload containing `user_email` and `message`.

    Returns:
        NotificationOut: The full notification metadata (ID, email, message, timestamp).

    Raises:
        HTTPException: If SNS publishing or DynamoDB saving fails.
    """
    # 1. Generate notification ID and timestamp
    notification_id = str(uuid4())
    sent_at = datetime.utcnow().isoformat()

    # 2. Publish to SNS
    try:
        sns_response = send_notification_to_sns(payload.user_email, payload.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send notification: {str(e)}")

    # 3. Save to DynamoDB
    try:
        await save_notification(notification_id, payload.user_email, payload.message, sent_at)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save notification: {str(e)}")

    # 4. Return response
    return NotificationOut(
        notification_id=notification_id,
        user_email=payload.user_email,
        message=payload.message,
        sent_at=datetime.fromisoformat(sent_at)
    )