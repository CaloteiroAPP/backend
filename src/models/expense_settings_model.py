from enum import Enum
from typing import List
from pydantic import BaseModel

from src.models.change_model import Change
from src.models.chat_model import Chat


class ExpenseType(Enum):
    ENTERTAINMENT = "entertainment"
    FOOD = "food"
    GENERAL = "general"
    SHOPPING = "shopping"
    TRANSPORT = "transport"


class SplittingMethod(Enum):
    CUSTOM_SPLITTING = "custom_splitting"
    EQUAL_SPLITTING = "equal_splitting"
    I_PAY_ALL = "i_pay_all"
    YOU_PAY_ALL = "you_pay_all"


class ExpenseSettings(BaseModel):
    activity: List[Change] = []
    description: str = ""
    method: str = SplittingMethod.EQUAL_SPLITTING
    photo: str | None = None
    type: str = ExpenseType.GENERAL
    chat: Chat | None = None
