# api/routes/chat.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from api.db.deps import get_db
from api.models.chat import Chat
from api.models.user import User
from api.schemas.chat import ChatListItem, ChatParticipant

router = APIRouter()

@router.get(
    "/chats",
    response_model=list[ChatListItem],
    summary="Get user chats",
    description="Returns all chats for a given user_sub as query param."
)
async def get_user_chats(user_sub: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Chat).where((Chat.user1_sub == user_sub) | (Chat.user2_sub == user_sub))
    )
    chats = result.scalars().all()

    chat_items = []
    for chat in chats:
        other_user_sub = chat.user2_sub if chat.user1_sub == user_sub else chat.user1_sub
        user_result = await db.execute(select(User).where(User.sub == other_user_sub))
        other_user = user_result.scalar_one_or_none()

        if other_user:
            chat_items.append(ChatListItem(
                id=chat.id,
                participant=ChatParticipant(
                    first_name=other_user.first_name,
                    last_name=other_user.last_name
                )
            ))
    return chat_items
