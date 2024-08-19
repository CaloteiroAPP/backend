
from uuid import UUID
from pydantic import BaseModel


class Friend(BaseModel):
    favorite: bool = False
    user: UUID
