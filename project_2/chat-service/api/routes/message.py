# api/routes/message.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from api.db.deps import get_db
from api.models.message import Message
from api.models.chat import Chat
from api.schemas.message import MessageCreateIn, MessageOut


# Create a router instance to handle message-related routes
router = APIRouter()

@router.post(
    "/messages",
    response_model=MessageOut,
    summary="Create new message",
    description=(
        "Creates a new message in the system. "
        "Supports both plain text messages and messages with attached media. "
        "If both text and media are provided, they will be saved together as a single message."
    ),
    responses={
        200: {"description": "Message created successfully"},
        400: {"description": "Invalid input data"},
        500: {"description": "Internal server error while saving the message"}
    },
    tags=["Messages"]
)
async def create_message(
    payload: MessageCreateIn,
    db: AsyncSession = Depends(get_db)
):
    """
    Creates and stores a new message in the database.

    Accepts data from either the frontend (user submitting a message) or
    the media-service (uploading a message with an image). The message
    can include just text, just media, or both.

    Parameters:
    - **payload**: Data for the new message (chat_id, sender_sub, content, media_url, media_id)
    - **db**: SQLAlchemy session injected via FastAPI dependency

    Returns:
    - The newly created `Message` object as a response schema (`MessageOut`)
    """
    # Construct SQLAlchemy model instance from payload
    message = Message(
        chat_id=payload.chat_id,
        sender_sub=payload.sender_sub,
        content=payload.content,
        media_url=payload.media_url,
        media_id=payload.media_id
    )

    # Persist the message in the database
    db.add(message)
    await db.commit()
    await db.refresh(message)

    return message


@router.get(
    "/messages/{chat_id}",
    response_model=list[MessageOut],
    summary="Get messages from a chat",
    description="Retrieves all messages from a given chat, ordered by time sent."
)
async def get_chat_messages(chat_id: int, db: AsyncSession = Depends(get_db)):
    # Check if the chat exists
    result = await db.execute(select(Chat).where(Chat.id == chat_id))
    chat = result.scalar_one_or_none()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    # Retrieve and return messages
    result = await db.execute(
        select(Message).where(Message.chat_id == chat_id).order_by(Message.sent_at)
    )
    return result.scalars().all()