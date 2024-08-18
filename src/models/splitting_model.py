from uuid import UUID
from pydantic import BaseModel

from src.models.splitting_settings_model import SplitingSettings

    
class Spliting(BaseModel):
    amount: float
    settings: SplitingSettings = SplitingSettings()
    user: UUID