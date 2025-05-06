# api/schemas/message.py

from pydantic import BaseModel, Field, model_validator
from typing import Optional
from uuid import UUID
from datetime import datetime


class MessageCreateIn(BaseModel):
    """
    Schema representing the payload for creating a new message.

    This can be a simple text message, a message containing media (image/video), or both.
    It is used by both frontend clients and internal services like media-service.
    """
    chat_id: int = Field(..., description="ID of the conversation/chat where the message is sent")
    sender_sub: str = Field(..., description="Cognito 'sub' of the user sending the message")
    content: Optional[str] = Field(None, description="Text content of the message (can be empty if media-only)")
    media_url: Optional[str] = Field(None, description="URL to the uploaded media file, if any")
    media_id: Optional[UUID] = Field(None, description="UUID of the media file stored in DynamoDB")

    @model_validator(mode="after")
    def check_at_least_content_or_media(self) -> "MessageCreateIn":
        """
        Ensure that at least one of 'content' or 'media_url' is provided.
        """
        if not self.content and not self.media_url:
            raise ValueError("Message must contain either 'content' or 'media_url'")
        return self


class MessageOut(BaseModel):
    """
    Schema representing a message in a chat.

    Includes basic information such as message ID, sender, content, and timestamp.
    Can represent both text and media messages.
    """
    id: int = Field(..., description="Unique identifier of the message")
    chat_id: int = Field(..., description="ID of the chat the message belongs to")
    sender_sub: str = Field(..., description="Cognito 'sub' of the user who sent the message")
    content: Optional[str] = Field(None, description="Message text content (optional for media-only messages)")
    media_url: Optional[str] = Field(None, description="URL to the media file, if the message includes one")
    media_id: Optional[UUID] = Field(None, description="UUID of the media file stored in external service")
    sent_at: datetime = Field(..., description="Timestamp when the message was created (UTC)")

    class Config:
        from_attributes = True  # Enables ORM mode for SQLAlchemy integration