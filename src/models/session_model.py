
from enum import Enum
from typing import List
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

class SessionSettings:
    photo: str

    class Config:
        orm_mode = True
        
class Session(BaseModel):
    _id: UUID
    password: UUID = uuid4()
    public_code: UUID = uuid4()
    type: SessionType
    settings: SessionSettings
    
    expenses: List[UUID] = []
    users: List[UUID] = []
    session_activity: List[UUID] = []
        
        
        