from enum import Enum
from pydantic import BaseModel

from src.models.chat_model import Chat


class SessionType(Enum):
    COUPLE = "couple"
    ENTERTAINMENT = "entertainment"
    GENERAL = "general"
    GROUP = "group"
    HOME = "home"
    TRIP = "trip"
    WORK = "work"


class SessionSettings(BaseModel):
    chat: Chat = Chat()
    photo: str = None
    # temporary_access:  #TODO: Implement this
    # public_code:  #TODO: Implement this
    type: str = SessionType.GENERAL
    
    class Config:
        arbitrary_types_allowed = True
