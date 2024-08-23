
from bson import ObjectId
from pydantic import BaseModel

from src.models.session_settings_model import SessionType


class CreateSessionDTO(BaseModel):
    creator: ObjectId
    creator_password: str
    name: str
    photo: str
    type: str = SessionType.GENERAL
    
    class Config:
        arbitrary_types_allowed = True
