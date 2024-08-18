
from typing import List
from uuid import UUID

from pydantic import BaseModel

from src.models.user_settings_model import UserSettings


class User(BaseModel):
    _id: UUID
    email: str
    first_name: str
    last_name: str
    password: str
    personal_activity: List[UUID] = []
    sessions: List[UUID] = []
    user_settings: UserSettings = UserSettings()

