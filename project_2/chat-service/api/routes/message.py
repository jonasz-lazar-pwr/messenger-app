# api/routes/message.py

"""
Routes for message-related operations.

This module handles message creation (text, media, or both) and retrieval of messages for a given chat.

Endpoints:
- POST /api/messages: Create a new message (with optional media upload to media-service).
- GET /api/messages/{chat_id}: Retrieve all messages from a specific chat, ordered by time sent.
"""

import httpx
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional
from api.db.deps import get_db
from api.models.message import Message
from api.models.chat import Chat
from api.schemas.message import MessageOut
from api.services.notification import send_notification_for_message
from api.core.config import settings
from uuid import UUID

# Create a router instance to handle message-related routes
router = APIRouter()


@router.post(
    "",
    response_model=MessageOut,
    summary="Create new message",
    description=(
        "Creates a new message in the system. Supports:\n"
        "- plain text messages,\n"
        "- media messages (file upload),\n"
        "- or both together.\n\n"
        "If a file is uploaded, the chat-service will internally forward the file "
        "to the media-service for S3 upload and metadata storage."
    ),
    responses={
        200: {"description": "Message created successfully"},
        400: {"description": "Invalid input data"},
        500: {"description": "Internal server error while processing the message"}
    },
    tags=["Messages"]
)
async def create_message(
    chat_id: int = Form(...),
    sender_sub: str = Form(...),
    content: Optional[str] = Form(None),
    media_file: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new message (text, media, or both).

    This endpoint allows users to send plain text messages, media files (images), or both.
    If a media file is provided, it is forwarded to the media-service for S3 upload and metadata storage.

    Validation:
    - Requires at least text or media (cannot be empty).
    - Only image files are accepted as media (content type must start with 'image/').

    On success, the message is stored in the database, and a notification is triggered.

    Args:
        chat_id (int): ID of the chat where the message is sent.
        sender_sub (str): Cognito sub (UUID) of the sender.
        content (Optional[str]): Optional text content of the message.
        media_file (Optional[UploadFile]): Optional uploaded file (only images allowed).
        db (AsyncSession): SQLAlchemy async database session (injected).

    Returns:
        MessageOut: The created message, serialized using the MessageOut schema.

    Raises:
        HTTPException:
            - 400: If both text and media are missing, or if invalid media type.
            - 404: If the specified chat does not exist.
            - 500: On unexpected errors (e.g., media upload failure, notification failure).
    """
    # Ensure that at least text content or a media file is provided
    if not (content and content.strip()) and not media_file:
        raise HTTPException(status_code=400, detail="Message must contain text or a media file")

    media_url = None
    media_id = None

    if media_file:
        # Validate the media file type (accept only images based on content type)
        if media_file.content_type is None or not media_file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Only image files are allowed")

        # Prepare multipart/form-data request to the media-service for file upload
        form_data = {
            "file": (media_file.filename, media_file.file, media_file.content_type)
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    f"http://{settings.MEDIA_SERVICE_HOST}:{settings.MEDIA_SERVICE_PORT}/api/media/upload",
                    files=form_data
                )
            response.raise_for_status()
            media_response = response.json()
            media_url = media_response["url"]
            media_id = media_response["id"]
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=400, detail=f"Media upload rejected: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to upload media: {str(e)}")

    # Check if the specified chat exists in the database
    chat_result = await db.execute(select(Chat).where(Chat.id == chat_id))
    chat = chat_result.scalar_one_or_none()
    if chat is None:
        raise HTTPException(status_code=404, detail="Chat not found")

    # Save the new message to the database
    message = Message(
        chat_id=chat_id,
        sender_sub=sender_sub,
        content=content,
        media_url=media_url,
        media_id=UUID(media_id) if media_id else None
    )

    db.add(message)
    await db.commit()
    await db.refresh(message)

    # Send notification to participants after the message is saved
    try:
        await send_notification_for_message(
            db=db,
            sender_sub=sender_sub,
            message_content=content,
            has_media=bool(media_url)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send notification: {str(e)}")

    return message


@router.get(
    "/{chat_id}",
    response_model=list[MessageOut],
    summary="Get messages from a chat",
    description="Retrieves all messages from a given chat, ordered by time sent."
)
async def get_chat_messages(chat_id: int, db: AsyncSession = Depends(get_db)):
    """
    Retrieve all messages from a specific chat.

    This endpoint returns a list of messages for the given chat ID, ordered chronologically by send time.

    Args:
        chat_id (int): ID of the chat whose messages are to be retrieved.
        db (AsyncSession): SQLAlchemy async database session (injected).

    Returns:
        list[MessageOut]: List of messages in the specified chat.

    Raises:
        HTTPException:
            - 404: If the chat with the given ID does not exist.
    """
    # Check if the chat exists in the database
    result = await db.execute(select(Chat).where(Chat.id == chat_id))
    chat = result.scalar_one_or_none()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    # Retrieve all messages for the chat, ordered by sent_at timestamp
    result = await db.execute(
        select(Message).where(Message.chat_id == chat_id).order_by(Message.sent_at)
    )
    return result.scalars().all()