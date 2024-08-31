

from pydantic import BaseModel
from src.models.user_model import User


class FriendRequest(BaseModel):
    user: User
    friend: User
