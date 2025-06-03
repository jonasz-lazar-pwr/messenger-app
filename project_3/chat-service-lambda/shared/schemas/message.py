# === shared/schemas/message.py ===

"""Pydantic schemas related to chat messages.

Includes models for sending and receiving text and media messages.
"""

from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime


class MessageOut(BaseModel):
    """
    Schema representing a single message returned to the client.

    A message may include text content, a media file, or both.
    """

    id: int = Field(..., description="Unique identifier of the message")
    chat_id: int = Field(..., description="ID of the chat this message belongs to")
    sender_sub: str = Field(..., description="Cognito subject identifier (sub) of the sender")
    content: Optional[str] = Field(None, description="Text content of the message, if present")
    media_url: Optional[str] = Field(None, description="Public URL of the uploaded media file, if present")
    media_id: Optional[UUID] = Field(None, description="UUID of the media file stored in external storage")
    sent_at: datetime = Field(..., description="UTC timestamp when the message was created")

    class Config:
        from_attributes = True


class MessageTextIn(BaseModel):
    """
    Schema for sending a plain text message.

    Used in POST /api/messages/text requests.
    """

    chat_id: int = Field(..., description="ID of the chat to which the message is sent")
    content: str = Field(..., min_length=1, description="Non-empty text content of the message")

    class Config:
        from_attributes = True


class MessageMediaIn(BaseModel):
    """
    Schema for sending a media message (e.g., image, video).

    Sent via multipart/form-data; this model captures form field metadata.
    """

    chat_id: int = Field(..., description="ID of the chat to which the media message is sent")
    sender_sub: str = Field(..., description="Cognito subject identifier (sub) of the sender")

    class Config:
        from_attributes = True