

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel

from src.models.change_model import Change
from src.models.chat_model import Chat

class ExpenseType(Enum):
    ENTERTAINMENT = "entertainment"
    FOOD = "food"
    GENERAL = "general"
    SHOPPING = "shopping"
    TRANSPORT = "transport"

class ExpenseSettings(BaseModel):
    activity: List[Change] = []
    description: str = ""
    photo: Optional[str] = None
    type: ExpenseType = ExpenseType.GENERAL
    chat: Optional[Chat] = None