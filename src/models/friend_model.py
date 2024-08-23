
from bson import ObjectId
from pydantic import BaseModel


class Friend(BaseModel):
    favorite: bool = False
    user: ObjectId
    
    class Config:
        arbitrary_types_allowed = True
