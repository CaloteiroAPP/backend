from enum import Enum
from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel


class SessionType(Enum):
    GENERAL = "general"
    TRIP = "trip"
    ENTERTAINMENT = "entertainment"
    GROUP = "group"
    HOME = "home"
    COUPLE = "couple"
    WORK = "work"


class SessionSettings(BaseModel):
    chat: Optional[UUID] = None
    photo: str
    temporary_access: UUID = uuid4()
    type: SessionType = SessionType.GENERAL
