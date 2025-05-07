# api/schemas/notification_item.py

from pydantic import BaseModel, Field, constr
from datetime import datetime


class SendNotificationIn(BaseModel):
    user_email: str = Field(..., description="Email address of the user who will receive the notification.")
    message: constr(min_length=1) = Field(..., description="The content of the notification message")

class NotificationOut(BaseModel):
    notification_id: str = Field(..., description="Unique identifier for the notification (UUID4).")
    user_email: str = Field(..., description="Email address of the user who received the notification.")
    message: str = Field(..., description="The body content of the notification message.")
    sent_at: datetime = Field(..., description="UTC timestamp indicating when the notification was sent.")