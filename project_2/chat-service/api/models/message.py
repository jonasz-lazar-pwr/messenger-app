# api/models/message.py

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Text, func
from sqlalchemy.orm import relationship
from .base import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id", ondelete="CASCADE"))
    sender_sub = Column(String, ForeignKey("users.sub"), nullable=False)
    content = Column(Text, nullable=True)
    media_url = Column(String, nullable=True)
    media_id = Column(UUID(as_uuid=True), nullable=True)
    sent_at = Column(DateTime, server_default=func.now())

    chat = relationship(
        "Chat",
        back_populates="messages"
    )