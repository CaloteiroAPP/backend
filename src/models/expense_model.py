
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

class State(Enum):
    WAITING_PAYMENTS = "waiting_payments"
    SETTLED_UP = "settled_up"
    # TODO: Check if there are more states 

class ExpenseType(Enum):
    GENERAL = "general"
    FOOD = "food"
    TRANSPORT = "transport"
    ENTERTAINMENT = "entertainment"
    SHOPPING = "shopping"
    # TODO: Add more expense types
    
class Change:
    str: str
    timestamp: int
    
class Spliting:
    user: UUID
    amount: float
    reaction: Optional[str] = None
    
# class Currency:
#     code: str
    
class Expense(BaseModel):
    _id: UUID
    payer: UUID
    amount: float
    currency: str
    state: State
    description: str
    type: ExpenseType
    timestamp: int
    
    changes: List[Change] = []
    
    session: Optional[str] = None
    spliting: List[Spliting]

    class Config:
        orm_mode = True
        

    