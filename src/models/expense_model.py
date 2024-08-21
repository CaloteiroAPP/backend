import time
from enum import Enum
from typing import List
from uuid import UUID, uuid4

from pydantic import BaseModel

from src.models.expense_settings_model import ExpenseSettings
from src.models.splitting_model import Splitting


class State(Enum):
    SETTLED_UP = "settled_up"
    WAITING_PAYMENTS = "waiting_payments"


class Expense(BaseModel):
    _id: UUID = uuid4()
    amount: float
    currency: str
    expense_settings: ExpenseSettings = ExpenseSettings()
    payer: UUID
    session: UUID | None = None
    splitting: List[Splitting]
    state: str = State.WAITING_PAYMENTS
    timestamp: float = time.time()
    
    # TODO: Remove this method
    def model_dump(self, **kwargs): 
        data = super().model_dump(**kwargs)
        data["_id"] = self._id
        return data
