

from pydantic import BaseModel


class CreateUserDTO(BaseModel):
    email: str
    first_name: str
    last_name: str
    password: str
    phone: int | None = None
    photo: str | None = None
    
    class Config:
        arbitrary_types_allowed = True
