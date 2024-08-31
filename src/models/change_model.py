import time

from pydantic import BaseModel


class Change(BaseModel):
    change_message: str
    timestamp: float = time.time()
    
    class Config:
        arbitrary_types_allowed = True
