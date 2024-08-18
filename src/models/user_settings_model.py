

from typing import Optional
from uuid import UUID
from pydantic import BaseModel

from src.models.notification_settings_model import NotificationSettings


class UserSettings(BaseModel):
    app_access_code: Optional[int] = None
    blocked_users: list[UUID] = []
    muted_users: list[UUID] = []
    notification_settings: NotificationSettings = NotificationSettings()
    verified: bool = False