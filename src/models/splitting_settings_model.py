
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class SplitingState(Enum):
    WAITING = "waiting"
    DONE = "done"
    PAID = "paid"
    REJECTED = "rejected"

class SplitingSettings(BaseModel):
    reaction: Optional[str] = None
    state: SplitingState = SplitingState.WAITING