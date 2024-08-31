from bson import ObjectId
from pydantic import BaseModel

from src.models.splitting_settings_model import SplittingSettings


class Splitting(BaseModel):
    amount: float
    settings: SplittingSettings = SplittingSettings()
    user_id: ObjectId
    
    class Config:
        arbitrary_types_allowed = True
