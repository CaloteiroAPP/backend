
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from src.models.user_settings_model import UserSettings


class Friend(BaseModel):
    user: UUID
    favorite: bool

class User(BaseModel):
    _id: UUID
    email: str
    password: str
    phone: Optional[int] = None
    first_name: str
    last_name: str
    
    friends: List[Friend] = []
    
    sessions: List[UUID] = []
    personal_activity: List[UUID] = []
    
    user_settings: UserSettings = UserSettings()

