

from src.repositories.notification_repository import NotificationRepository
from src.services.service_interface import ServiceInterface


class NotificationService(ServiceInterface):
    def __init__(self, notification_repository: NotificationRepository):
        super().__init__(notification_repository)