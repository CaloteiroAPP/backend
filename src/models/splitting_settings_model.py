from enum import Enum
from typing import Optional

from pydantic import BaseModel


class SplittingState(Enum):
    WAITING = "waiting"
    DONE = "done"
    PAID = "paid"
    REJECTED = "rejected"


class SplittingSettings(BaseModel):
    reaction: Optional[str] = None
    state: SplittingState = SplittingState.WAITING
