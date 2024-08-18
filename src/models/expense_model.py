from enum import Enum
import time
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class State(Enum):
    WAITING_PAYMENTS = "waiting_payments"
    SETTLED_UP = "settled_up"

class SplitingState(Enum):
    WAITING = "waiting"
    DONE = "done"
    PAID = "paid"
    REJECTED = "rejected"

class ExpenseType(Enum):
    GENERAL = "general"
    FOOD = "food"
    TRANSPORT = "transport"
    ENTERTAINMENT = "entertainment"
    SHOPPING = "shopping"

class Change(BaseModel):
    str: str
    timestamp: float = time.time()

class Spliting(BaseModel):
    user: UUID
    amount: float
    reaction: Optional[str] = None
    state: SplitingState

class Expense(BaseModel):
    _id: UUID
    payer: UUID
    amount: float
    currency: str
    state: State
    description: str
    type: ExpenseType
    timestamp: float = time.time()
    
    changes: List[Change] = []
    
    session: Optional[str] = None
    spliting: List[Spliting]
