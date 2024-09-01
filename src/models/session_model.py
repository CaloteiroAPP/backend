import random
import string
import time
from typing import List

from bson import ObjectId
from pydantic import BaseModel, Field

from src.models.change_model import Change
from src.models.session_settings_model import SessionSettings


def generate_session_password(length=6):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


class Session(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId)
    activity: List[Change] = []
    creator: ObjectId
    expenses: List[ObjectId] = []
    members: List[ObjectId] = []
    name: str
    password: str = generate_session_password()
    session_settings: SessionSettings = SessionSettings()
    timestamp: float = time.time()
    
    class Config:
        arbitrary_types_allowed = True

