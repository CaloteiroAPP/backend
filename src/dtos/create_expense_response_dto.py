
from pydantic import BaseModel


class CreateExpenseResponseDTO(BaseModel):
    id: str | None = None
