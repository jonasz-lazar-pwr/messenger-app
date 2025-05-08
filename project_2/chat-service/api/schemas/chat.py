# api/schemas/chat.py

from pydantic import BaseModel, Field


class ChatParticipant(BaseModel):
    """Basic information about the other participant in a chat."""
    first_name: str = Field(..., description="First name of the participant")
    last_name: str = Field(..., description="Last name of the participant")

    class Config:
        from_attributes = True


class ChatListItem(BaseModel):
    """Schema representing a single chat entry in the user's chat list."""
    id: int = Field(..., description="Unique ID of the chat")
    participant: ChatParticipant = Field(..., description="Information about the other participant in the chat")

    class Config:
        from_attributes = True
