import time
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from src.models.change_model import Change
from src.models.chat_model import Chat
from src.models.splitting_model import Spliting


class State(Enum):
    WAITING_PAYMENTS = "waiting_payments"
    SETTLED_UP = "settled_up"

class ExpenseType(Enum):
    GENERAL = "general"
    FOOD = "food"
    TRANSPORT = "transport"
    ENTERTAINMENT = "entertainment"
    SHOPPING = "shopping"

class Expense(BaseModel):
    _id: UUID
    payer: UUID
    amount: float
    currency: str
    state: State
    description: str
    photo: Optional[str] = None
    type: ExpenseType
    timestamp: float = time.time()
    
    changes: List[Change] = []
    chat: Optional[Chat] = None
    
    session: Optional[str] = None
    spliting: List[Spliting]
