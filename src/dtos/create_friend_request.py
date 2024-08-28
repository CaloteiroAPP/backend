
from pydantic import BaseModel


class CreateFriendRequestDTO(BaseModel):
    user_email: str
    user_password: str
    friend_email: str
