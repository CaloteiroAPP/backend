
from pydantic import BaseModel


class NotificationSettings(BaseModel):
    allow_notifications: bool = True
    # email_notifications: bool = True
    # push_notifications: bool = True
    # sms_notifications: bool = True
    
    # TODO: Add more notification settings
