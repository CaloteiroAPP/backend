from enum import Enum
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class SplitingState(Enum):
    WAITING = "waiting"
    DONE = "done"
    PAID = "paid"
    REJECTED = "rejected"
    
class Spliting(BaseModel):
    user: UUID
    amount: float
    reaction: Optional[str] = None
    state: SplitingState