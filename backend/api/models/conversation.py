from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, func
from sqlalchemy.orm import relationship
from .base import Base

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user1_sub = Column(String, ForeignKey("users.sub"), nullable=False)
    user2_sub = Column(String, ForeignKey("users.sub"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    user1 = relationship(
        "User",
        foreign_keys=[user1_sub],
        back_populates="conversations_as_user1"
    )
    user2 = relationship(
        "User",
        foreign_keys=[user2_sub],
        back_populates="conversations_as_user2"
    )

    messages = relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete"
    )
