
from typing import List
from bson import ObjectId
from src.models.notification_model import Notification, NotificationType
from src.repositories.notification_repository import NotificationRepository


class NotificationService:
    def __init__(self, notification_repository: NotificationRepository):
        self.repository = notification_repository
        
    def create_notification(self, notification: Notification) -> Notification:
        return self.repository.create_notification(notification)
    
    def create_notifications(self, notifications: List[Notification]) -> List[Notification]:
        return self.repository.create_notifications(notifications)

    @staticmethod
    def create_notifications_list(users: List[ObjectId], n_type: NotificationType, session: ObjectId = None, data=None) -> List[Notification]:
        if data is None:
            data = {}
        notifications = []
        for user_id in users:
            notifications.append(Notification(user_id=user_id, session=session, data=data, type=n_type))
        return notifications
