
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from src.models.friend_model import Friend
from src.models.user_settings_model import UserSettings


class User(BaseModel):
    _id: UUID
    email: str
    first_name: str
    friends: List[Friend] = []
    friend_requests: List[UUID] = []
    last_name: str
    password: str
    personal_activity: List[UUID] = []
    phone: Optional[int] = None
    sessions: List[UUID] = []
    user_settings: UserSettings = UserSettings()

