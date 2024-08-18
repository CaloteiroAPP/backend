import time
from uuid import UUID

from pydantic import BaseModel


class Message(BaseModel):
    text: str
    user: UUID
    timestamp: float = time.time()