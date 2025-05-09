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
from api.db.deps import get_db
from api.models.message import Message
from api.models.chat import Chat
from api.schemas.message import MessageOut, MessageTextIn
from api.services.notification import send_notification_for_message
from api.core.config import settings
from uuid import UUID
import traceback

# Create a router instance to handle message-related routes
router = APIRouter()

@router.post(
    "/text",
    response_model=MessageOut,
    summary="Create new text message",
    description="Creates a new text-only message (no media allowed).",
    responses={
        200: {"description": "Text message created successfully"},
        400: {"description": "Invalid input data (e.g., missing content)"},
        404: {"description": "Chat not found"},
        500: {"description": "Unexpected server error"}
    },
    tags=["Messages"]
)
async def create_text_message(
    message_in: MessageTextIn,
    db: AsyncSession = Depends(get_db)
):
    """
    Creates a **text-only message** in the given chat.

    Validation:
    - Requires non-empty `content`.
    """
    if not message_in.content or not message_in.content.strip():
        raise HTTPException(status_code=400, detail="Message content cannot be empty")

    # Check chat exists
    chat_result = await db.execute(select(Chat).where(Chat.id == message_in.chat_id))
    chat = chat_result.scalar_one_or_none()
    if chat is None:
        raise HTTPException(status_code=404, detail="Chat not found")

    message = Message(
        chat_id=message_in.chat_id,
        sender_sub=message_in.sender_sub,
        content=message_in.content,
        media_url=None,
        media_id=None
    )

    db.add(message)
    await db.commit()
    await db.refresh(message)

    try:
        await send_notification_for_message(
            db=db,
            sender_sub=message_in.sender_sub,
            message_content=message_in.content,
            has_media=False
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload media: {str(e)}")

    return message


@router.post(
    "/media",
    response_model=MessageOut,
    summary="Create new media message",
    description="Creates a new message that contains ONLY media (no text allowed).",
    responses={
        200: {"description": "Media message created successfully"},
        400: {"description": "Invalid input data (e.g., missing media, invalid file type)"},
        404: {"description": "Chat not found"},
        500: {"description": "Unexpected server error"}
    },
    tags=["Messages"]
)
async def create_media_message(
    chat_id: int = Form(...),
    sender_sub: str = Form(...),
    media_file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    """
    Creates a media-only message (no text allowed).
    """
    if media_file.content_type is None or not media_file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed")

    # Upload to media-service
    form_data = {
        "file": (media_file.filename, media_file.file, media_file.content_type)
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"http://{settings.MEDIA_SERVICE_HOST}:{settings.MEDIA_SERVICE_PORT}/media/upload",
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

    # Check chat exists
    chat_result = await db.execute(select(Chat).where(Chat.id == chat_id))
    chat = chat_result.scalar_one_or_none()
    if chat is None:
        raise HTTPException(status_code=404, detail="Chat not found")

    message = Message(
        chat_id=chat_id,
        sender_sub=sender_sub,
        content=None,
        media_url=media_url,
        media_id=UUID(media_id)
    )

    db.add(message)
    await db.commit()
    await db.refresh(message)

    try:
        await send_notification_for_message(
            db=db,
            sender_sub=sender_sub,
            message_content=None,
            has_media=True
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload media: {str(e)}")

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
