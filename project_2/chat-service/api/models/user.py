# api/models/user.py

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from .base import Base

class User(Base):
    __tablename__ = "users"

    sub = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

    chats_as_user1 = relationship(
        "Chat",
        back_populates="user1",
        foreign_keys="Chat.user1_sub"
    )
    chats_as_user2 = relationship(
        "Chat",
        back_populates="user2",
        foreign_keys="Chat.user2_sub"
    )
