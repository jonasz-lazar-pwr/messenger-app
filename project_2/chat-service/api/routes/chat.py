# api/routes/chat.py

"""
Routes for chat-related operations.

This module provides an endpoint to retrieve all chats for a specific user,
returning minimal chat info along with the other participant's details.

Endpoints:
- GET /api/chats: Retrieve all chats for a given user_sub (query param).
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
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
    description="Returns all chats for a given user_sub as query param."
)
async def get_user_chats(user_sub: str, db: AsyncSession = Depends(get_db)):
    """
    Retrieve all chats for a specific user.

    This endpoint fetches all chats where the user participates (either as user1 or user2),
    and for each chat, it includes the basic details of the other participant.

    Args:
        user_sub (str): Cognito sub (UUID) of the user for whom to retrieve chats.
        db (AsyncSession): SQLAlchemy async database session (injected).

    Returns:
        list[ChatListItem]: List of chats with minimal information (chat ID and participant's name).

    Example response:
    ```json
    [
        {
            "id": 1,
            "participant": {
                "first_name": "Alice",
                "last_name": "Wonder"
            }
        },
        {
            "id": 2,
            "participant": {
                "first_name": "Bob",
                "last_name": "Builder"
            }
        }
    ]
    ```

    Notes:
    - If the user is in no chats, an empty list is returned.
    - Only chats where both participants exist in the database are included in the response.
    """
    # Query for chats where the user participates as user1 or user2
    result = await db.execute(
        select(Chat).where((Chat.user1_sub == user_sub) | (Chat.user2_sub == user_sub))
    )
    chats = result.scalars().all()

    chat_items = []

    # For each chat, determine the other participant and fetch their details
    for chat in chats:
        other_user_sub = chat.user2_sub if chat.user1_sub == user_sub else chat.user1_sub
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
