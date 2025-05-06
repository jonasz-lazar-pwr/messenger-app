# api/models/chat.py

from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, func
from sqlalchemy.orm import relationship
from .base import Base

class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    user1_sub = Column(String, ForeignKey("users.sub"), nullable=False)
    user2_sub = Column(String, ForeignKey("users.sub"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    user1 = relationship(
        "User",
        foreign_keys=lambda: [Chat.user1_sub],
        back_populates="chats_as_user1"
    )
    user2 = relationship(
        "User",
        foreign_keys=lambda: [Chat.user2_sub],
        back_populates="chats_as_user2"
    )

    messages = relationship(
        "Message",
        back_populates="chat",
        cascade="all, delete"
    )