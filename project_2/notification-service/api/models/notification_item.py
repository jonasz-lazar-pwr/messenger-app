# api/models/notification_item.py

from pydantic import BaseModel
from datetime import datetime

class NotificationItem(BaseModel):
    notification_id: str
    user_email: str
    message: str
    sent_at: datetime