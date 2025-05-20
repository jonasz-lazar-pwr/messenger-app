from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Text, func
from sqlalchemy.orm import relationship
from .base import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id", ondelete="CASCADE"))
    sender_sub = Column(String, ForeignKey("users.sub"), nullable=False)
    content = Column(Text)
    sent_at = Column(DateTime, server_default=func.now())

    conversation = relationship(
        "Conversation",
        back_populates="messages"
    )