
from enum import Enum
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel

from src.models.change_model import Change
from src.models.session_settings_model import SessionSettings


class SessionType(Enum):
    GENERAL = "general"
    TRIP = "trip"
    ENTERTAINMENT = "entertainment"
    GROUP = "group"
    HOME = "home"
    COUPLE = "couple"
    WORK = "work"

class Session(BaseModel):
    _id: UUID
    password: UUID = uuid4()
    public_code: UUID = uuid4()
    type: SessionType
    settings: SessionSettings
    
    chat: Optional[UUID] = None
    changes: List[Change] = []
    
    expenses: List[UUID] = []
    users: List[UUID] = []
    session_activity: List[UUID] = []
        