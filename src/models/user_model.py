
from typing import List

from bson import ObjectId
from pydantic import BaseModel, Field

from src.models.user_settings_model import UserSettings


class User(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId)
    email: str
    first_name: str
    last_name: str
    full_name: str
    password: str
    sessions: List[ObjectId] = []
    user_settings: UserSettings = UserSettings()
    
    class Config:
        arbitrary_types_allowed = True
