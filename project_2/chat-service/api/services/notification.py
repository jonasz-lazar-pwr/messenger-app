# api/services/notification.py

"""
Notification service integration module.

This module provides a utility function to send a notification
to the notification-service whenever a new message is created.

It retrieves sender details from the database and formats the notification
payload before dispatching it via HTTP.
"""

import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from api.core.config import settings
from api.models.user import User


async def send_notification_for_message(
    db: AsyncSession,
    sender_sub: str,
    message_content: str | None,
    has_media: bool
):
    """
    Send a notification to the notification-service about a new message.

    The function:
    1. Retrieves sender information from the database based on the Cognito sub.
    2. Builds a human-readable notification message including sender name,
       message content, and whether it includes media.
    3. Dispatches a POST request to the notification-service with the payload.

    Args:
        db (AsyncSession): The database session to fetch sender info.
        sender_sub (str): Cognito sub of the message sender.
        message_content (str | None): Text content of the message, if any.
        has_media (bool): Flag indicating if the message includes media (file/image).

    Returns:
        dict: The JSON response from the notification-service.

    Raises:
        httpx.HTTPStatusError: If the notification-service responds with an error status.
    """
    # 1. Get sender info from the database to personalize the notification
    result = await db.execute(select(User).where(User.sub == sender_sub))
    sender = result.scalar_one_or_none()

    if not sender:
        sender_name = f"Unknown ({sender_sub})"
    else:
        sender_name = f"{sender.first_name} {sender.last_name}"

    # 2. Build the notification message
    notification_message = (
        f"You have received a new message\n\n"
        f"From: {sender_name}\n"
        f"Message: {message_content or '[No text]'}\n"
        f"Contains media: {'Yes' if has_media else 'No'}"
    )

    payload = {
        "user_email": settings.NOTIFICATION_RECEIVER_EMAIL,
        "message": notification_message
    }

    # 3. Send POST request to the notification-service
    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.post(
            f"http://{settings.NOTIFICATION_SERVICE_HOST}:{settings.NOTIFICATION_SERVICE_PORT}/notifications/send/",
            json=payload
        )
        response.raise_for_status()
        return response.json()
