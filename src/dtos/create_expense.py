

import time
from typing import List
from uuid import UUID
from pydantic import BaseModel

from src.models.expense_model import ExpenseType, Spliting


class CreateExpense(BaseModel):
    payer: UUID
    amount: float
    currency: str
    description: str
    type: ExpenseType
    spliting: List[Spliting]
    
    class Config:
        orm_mode = True