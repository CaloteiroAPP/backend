
from typing import List
from uuid import UUID
from pydantic import BaseModel

from src.models.expense_model import Splitting, SplittingMethod
from src.models.expense_settings_model import ExpenseType


class CreateExpenseDTO(BaseModel):
    amount: float
    currency: str = "EUR"
    description: str = ""
    method: SplittingMethod = SplittingMethod.EQUAL_SPLITTING
    payer: UUID
    payer_password: str
    splitting: List[Splitting]
    session: UUID = None
    type: str = ExpenseType.GENERAL
    
    