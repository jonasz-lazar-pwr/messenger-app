# api/routes/chat.py

"""
This module provides an endpoint to retrieve all chats for the authenticated user,
returning minimal chat info along with the other participant's details.

Endpoints:
- GET /chats: Retrieve all chats for the authenticated user (using X-User-Payload header).
"""

import json
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from api.db.deps import get_db
from api.models.chat import Chat
from api.models.user import User
from api.schemas.chat import ChatListItem, ChatParticipant

# Create a router instance for chat-related routes
router = APIRouter()


@router.get(
    "",
    response_model=list[ChatListItem],
    summary="Get user chats",
    description=(
        "Returns all chats for the authenticated user based on the JWT payload "
        "passed via the X-User-Payload header."
    ),
    responses={
        200: {"description": "List of user chats"},
        400: {"description": "Invalid token payload"},
        422: {"description": "Missing X-User-Payload header"},
    }
)
async def get_user_chats(
    x_user_payload: str = Header(..., alias="X-User-Payload"),
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve all chats for the authenticated user.

    This endpoint fetches all chats where the authenticated user participates (either as user1 or user2),
    and for each chat, it includes the basic details of the other participant.

    The current user is identified from the `X-User-Payload` header, which must contain a JSON string
    with at least the 'sub' field.

    Args:
        x_user_payload (str): A JSON string provided via the X-User-Payload header,
            containing user identity attributes from the validated token.
        db (AsyncSession): The asynchronous database session (injected).

    Returns:
        list[ChatListItem]: List of chats with minimal information (chat ID and participant's name).

    Raises:
        HTTPException: 400 if the token payload is invalid or missing required fields.
        HTTPException: 422 if the X-User-Payload header is missing.
    """
    # Parse token payload to extract current user's sub
    try:
        payload = json.loads(x_user_payload)
        current_user_sub = payload.get("sub")
    except (json.JSONDecodeError, AttributeError):
        raise HTTPException(status_code=400, detail="Invalid X-User-Payload header")

    if not current_user_sub:
        raise HTTPException(status_code=400, detail="Missing 'sub' in token payload")

    # Query for chats where the current user is a participant
    result = await db.execute(
        select(Chat).where(
            (Chat.user1_sub == current_user_sub) | (Chat.user2_sub == current_user_sub)
        )
    )
    chats = result.scalars().all()

    chat_items = []

    # For each chat, determine the other participant and fetch their details
    for chat in chats:
        other_user_sub = chat.user2_sub if chat.user1_sub == current_user_sub else chat.user1_sub
        user_result = await db.execute(select(User).where(User.sub == other_user_sub))
        other_user = user_result.scalar_one_or_none()

        # Only include chats where the other user is found
        if other_user:
            chat_items.append(ChatListItem(
                id=chat.id,
                participant=ChatParticipant(
                    first_name=other_user.first_name,
                    last_name=other_user.last_name
                )
            ))

    return chat_items
