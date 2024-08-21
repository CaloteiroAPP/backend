

from typing import Collection, Optional
from uuid import UUID
from src.models.notification_model import Notification
from src.repositories.repository_interface import RepositoryInterface


class NotificationRepository(RepositoryInterface):
    
    def __init__(self, collection: Collection) -> None:
        super().__init__(collection)
        
    def verify_id_is_available(self, notification: Notification) -> bool:
        return super().verify_id_is_available(notification)
    
    def get_by_id(self, notification_id: UUID) -> Optional[dict]:
        return super().get_by_id(notification_id)
    
    def create(self, notification: Notification) -> Notification:
        notification_base_model = super().create(notification)
        return Notification(**notification_base_model.model_dump())
