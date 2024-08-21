from enum import Enum

from pydantic import BaseModel


class SplittingState(Enum):
    WAITING = "waiting"
    DONE = "done"
    PAID = "paid"
    REJECTED = "rejected"


class SplittingSettings(BaseModel):
    reaction: str | None = None
    state: SplittingState = SplittingState.WAITING
