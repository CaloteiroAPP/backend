import time
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from src.models.splitting_model import Splitting


class State(Enum):
    SETTLED_UP = "settled_up"
    WAITING_PAYMENTS = "waiting_payments"


class SplittingMethod(Enum):
    CUSTOM_SPLITTING = "custom_splitting"
    EQUAL_SPLITTING = "equal_splitting"
    I_PAY_ALL = "i_pay_all"
    YOU_PAY_ALL = "you_pay_all"


class Expense(BaseModel):
    _id: UUID
    amount: float
    currency: str
    method: SplittingMethod = SplittingMethod.EQUAL_SPLITTING
    payer: UUID
    session: Optional[str] = None
    splitting: List[Splitting]
    state: State = State.WAITING_PAYMENTS
    timestamp: float = time.time()
