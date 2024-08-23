
from typing import List
from bson import ObjectId
from pydantic import BaseModel

from src.models.expense_settings_model import ExpenseType, SplittingMethod
from src.models.splitting_model import Splitting


class CreateExpenseDTO(BaseModel):
    amount: float
    currency: str
    description: str = ""
    method: str = SplittingMethod.EQUAL_SPLITTING
    payer: ObjectId
    payer_password: str
    photo: str | None = None
    session: ObjectId | None = None
    splitting: List[Splitting]
    type: str = ExpenseType.GENERAL
    
    class Config:
        arbitrary_types_allowed = True
