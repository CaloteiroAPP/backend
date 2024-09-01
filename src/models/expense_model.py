import time
from enum import Enum
from typing import List

from bson import ObjectId
from pydantic import BaseModel, Field

from src.models.expense_settings_model import ExpenseSettings
from src.models.splitting_model import Splitting


class State(Enum):
    SETTLED_UP = "settled_up"
    WAITING_PAYMENTS = "waiting_payments"


class Expense(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId)
    amount: float
    currency: str
    expense_settings: ExpenseSettings = ExpenseSettings()
    payer_id: ObjectId
    session: ObjectId | None = None
    splitting: List[Splitting]
    state: str = State.WAITING_PAYMENTS
    timestamp: float = time.time()
    
    class Config:
        arbitrary_types_allowed = True
    
    # def model_dump_id(self, *args, **kwargs):  # TODO: Remove this method
    #     expense_dict = super().model_dump(*args, **kwargs)
    #     expense_dict['id'] = self.id
    #     return expense_dict
