
from functools import wraps
from pymongo.collection import Collection
from pymongo import errors
from bson import ObjectId
from src.models.notification_model import Notification
from src.repositories.repository_interface import RepositoryInterface


def handle_db_error(func):
    """Decorator to handle MongoDB related errors."""

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except errors.PyMongoError:
            return None

    return wrapper


class NotificationRepository(RepositoryInterface):
    
    def __init__(self, collection: Collection) -> None:
        super().__init__(collection)
        
    def verify_notification_id_is_available(self, notification: Notification) -> bool:
        notification_base_model = notification.model_dump()
        return super().verify_id_is_available(notification_base_model.get("id"))
    
    def get_notification_by_id(self, notification_id: ObjectId) -> dict | None:
        return super().get_by_id(notification_id)
    
    def create_notification(self, notification: Notification) -> Notification:
        notification_base_model = super().create(notification)
        return Notification(**notification_base_model.model_dump())
    
    def create_notifications(self, notifications: list[Notification]) -> list[Notification]:
        notifications_base_model = super().create_many(notifications)
        return [Notification(**notification_base_model.model_dump()) for notification_base_model in notifications_base_model]
    
