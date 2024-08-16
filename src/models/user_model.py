
from typing import List
from uuid import UUID

from pydantic import BaseModel


class NotificationSettings:
    email_notifications: bool = True
    push_notifications: bool = True
    sms_notifications: bool = True
    # TODO: Add more notification settings

class UserSettings:
    verified: bool
    app_access_code: int
    friends: list[UUID] = []
    blocked_users: list[UUID] = []
    muted_users: list[UUID] = []
    
    notification_settings: NotificationSettings

class User(BaseModel):
    _id: UUID
    email: str
    password: str
    phone: int
    first_name: str
    last_name: str
    photo_source: str
    
    sessions: List[UUID] = []
    personal_activity: List[UUID] = []
    
    user_settings: UserSettings

    class Config:
        orm_mode = True