
import random
import string
from typing import List
from bson import ObjectId
from pydantic import BaseModel

from src.models.friend_model import Friend
from src.models.notification_settings_model import NotificationSettings

def generate_user_friend_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

class UserSettings(BaseModel):
    app_access_code: int | None = None
    blocked_users: list[ObjectId] = []
    friend_code: str = generate_user_friend_code()
    friend_users: List[Friend] = []
    friend_requests: List[ObjectId] = []
    muted_users: list[ObjectId] = []
    notification_settings: NotificationSettings = NotificationSettings()
    phone: int | None = None
    photo: str | None = None
    verified: bool = False
    
    class Config:
        arbitrary_types_allowed = True
