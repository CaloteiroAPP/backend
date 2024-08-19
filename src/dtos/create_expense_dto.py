
from typing import List
from uuid import UUID
from pydantic import BaseModel

from src.models.expense_model import Splitting
from src.models.expense_settings_model import ExpenseType


class CreateExpenseDTO(BaseModel):
    payer: UUID
    amount: float
    currency: str
    description: str
    type: ExpenseType
    splitting: List[Splitting]
    
    class Config:
        orm_mode = True
