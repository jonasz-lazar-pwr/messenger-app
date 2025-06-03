# === shared/schemas/chat.py ===

"""Pydantic schemas related to chat resources.

Includes models for representing chat participants, chat list items,
and payloads for creating new chats.
"""

from pydantic import BaseModel, Field


class ChatParticipant(BaseModel):
    """
    Basic information about the other participant in a chat.

    Includes the first and last name of the user on the other side of the conversation.
    Used inside the `ChatListItem` model.
    """

    first_name: str = Field(..., description="First name of the participant")
    last_name: str = Field(..., description="Last name of the participant")

    class Config:
        from_attributes = True


class ChatListItem(BaseModel):
    """
    A single chat entry in the user's chat list.

    Returned by the GET /api/chats endpoint. Includes the chat ID
    and the basic data of the other participant.
    """

    id: int = Field(..., description="Unique identifier of the chat")
    participant: ChatParticipant = Field(..., description="Basic information about the other participant")

    class Config:
        from_attributes = True


class ChatCreate(BaseModel):
    """
    Request schema for creating a new chat.

    Used in POST /api/chats to initiate a new conversation
    by providing the Cognito 'sub' of the target user.
    """

    target_user_sub: str = Field(..., description="Cognito 'sub' of the target user")

    class Config:
        from_attributes = True