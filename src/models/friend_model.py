
from bson import ObjectId
from pydantic import BaseModel


class Friend(BaseModel):
    favorite: bool = False
    user_id: ObjectId
    
    class Config:
        arbitrary_types_allowed = True
