from typing import List
from pydantic import BaseModel

from src.models.expense_settings_model import ExpenseType, SplittingMethod
from src.models.splitting_settings_model import SplittingSettings


class CreateExpenseSplittingDto(BaseModel):
    amount: float
    settings: SplittingSettings = SplittingSettings()
    user_id: str


class CreateExpenseDTO(BaseModel):
    amount: float
    currency: str
    description: str = ""
    method: str = SplittingMethod.EQUAL_SPLITTING
    payer_id: str
    payer_password: str
    photo: str | None = None
    session: str | None = None
    splitting: List[CreateExpenseSplittingDto]
    type: str = ExpenseType.GENERAL

    class Config:
        arbitrary_types_allowed = True
