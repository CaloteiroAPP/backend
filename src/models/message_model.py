import time

from bson import ObjectId
from pydantic import BaseModel


class Message(BaseModel):
    text: str
    timestamp: float = time.time()
    sender: ObjectId
    
    class Config:
        arbitrary_types_allowed = True
