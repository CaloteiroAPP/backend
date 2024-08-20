

from src.repositories.user_repository import UserRepository
from src.services.service_interface import ServiceInterface


class UserService(ServiceInterface):
    def __init__(self, user_repository: UserRepository):
        super().__init__(user_repository)