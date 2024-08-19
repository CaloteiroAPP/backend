
from typing import List
from uuid import UUID
from pydantic import BaseModel

from src.models.expense_model import Splitting


class CreateExpenseDTO(BaseModel):
    payer: UUID
    amount: float
    currency: str
    description: str
    type: str
    splitting: List[Splitting]
    