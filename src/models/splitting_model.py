from uuid import UUID
from pydantic import BaseModel

from src.models.splitting_settings_model import SplittingSettings


class Splitting(BaseModel):
    amount: float
    settings: SplittingSettings = SplittingSettings()
    user: UUID
