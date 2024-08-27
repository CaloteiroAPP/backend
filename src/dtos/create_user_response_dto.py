

from src.models.user_model import User


class CreateUserResponseDTO(User):
    id: str | None = None
