

from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel

from src.models.friend_model import Friend
from src.models.notification_settings_model import NotificationSettings


class UserSettings(BaseModel):
    app_access_code: Optional[int] = None
    blocked_users: list[UUID] = []
    friends: List[Friend] = []
    friend_requests: List[UUID] = []
    muted_users: list[UUID] = []
    notification_settings: NotificationSettings = NotificationSettings()
    phone: Optional[int] = None
    verified: bool = False