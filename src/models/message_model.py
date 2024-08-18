import time
from uuid import UUID

from pydantic import BaseModel


class Message(BaseModel):
    text: str
    timestamp: float = time.time()
    sender: UUID