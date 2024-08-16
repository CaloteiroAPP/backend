
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class State(Enum):
    WAITING = "waiting"
    SETTLED = "settled"
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

class Expense(BaseModel):
    _id: UUID
    payer: UUID
    amount: float
    state: State
    description: str
    type: ExpenseType
    timestamp: int
    
    changes: List[Change] = []
    
    session: Optional[str] = None
    users: List[UUID] = []

    class Config:
        orm_mode = True
        

    