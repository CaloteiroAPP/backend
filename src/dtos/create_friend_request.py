
from pydantic import BaseModel


class CreateFriendRequestDTO(BaseModel):
    user_id: str
    user_password: str
    friend_id: str
