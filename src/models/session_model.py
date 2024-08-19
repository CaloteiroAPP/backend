import time
from typing import List
from uuid import UUID, uuid4

from pydantic import BaseModel

from src.models.change_model import Change
from src.models.session_settings_model import SessionSettings


class Session(BaseModel):
    _id: UUID = uuid4()
    activity: List[Change] = []
    creator: UUID
    expenses: List[UUID] = []
    members: List[UUID] = []
    name: str
    password: UUID = uuid4()
    public_code: UUID = uuid4()
    settings: SessionSettings = SessionSettings()
    timestamp: float = time.time()
