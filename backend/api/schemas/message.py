from pydantic import BaseModel, Field
from datetime import datetime

class MessageCreate(BaseModel):
    """Schema for creating a new message in a conversation."""
    conversation_id: int = Field(..., description="ID of the conversation")
    content: str = Field(..., description="Text content of the message")


class MessageOut(BaseModel):
    """Schema representing a message retrieved from a conversation."""
    id: int = Field(..., description="Unique message ID")
    conversation_id: int = Field(..., description="ID of the conversation this message belongs to")
    content: str | None = Field(None, description="Message content (may be null for media messages)")
    sender_sub: str = Field(..., description="Cognito 'sub' of the message sender")
    sent_at: datetime = Field(..., description="Timestamp when the message was sent")

    class Config:
        from_attributes = True