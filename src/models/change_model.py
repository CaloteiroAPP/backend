import time

from pydantic import BaseModel


class Change(BaseModel):
    str: str
    timestamp: float = time.time()
