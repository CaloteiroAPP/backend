

from src.repositories.session_repository import SessionRepository
from src.services.service_interface import ServiceInterface


class SessionService(ServiceInterface):
    def __init__(self, session_repository: SessionRepository):
        super().__init__(session_repository)