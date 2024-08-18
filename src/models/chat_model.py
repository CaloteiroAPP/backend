
import time
from uuid import UUID
from pydantic import BaseModel

class Message:
    text: str
    user: str
    timestamp: float = time.time()

class Chat(BaseModel):
    _id: UUID
    messages: list[Message] = []