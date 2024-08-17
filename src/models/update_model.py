
import time
from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class UpdateType(Enum):
    EXPENSE_PAYED = "expense_payed" # TODO: Implement this type
    EXPENSE_ADDED = "expense_added" # TODO: Implement this type
    EXPENSE_REMOVED = "expense_removed" # TODO: Implement this type
    EXPENSE_ERROR_DETECTED = "expense_error_detected" # TODO: Implement this type
    
    USER_JOINED_SESSION = "user_joined_session" # TODO: Implement this type
    NEW_SESSION_LINK = "new_session_link" # TODO: Implement this type
    SESSION_UPDATED = "session_updated" # TODO: Implement this type
    
    FRIEND_REQUEST_SENT = "friend_request_sent" # TODO: Implement this type
    FRIEND_REQUEST_ACCEPTED = "friend_request_accepted" # TODO: Implement this type
    FRIEND_REQUEST_REJECTED = "friend_request_rejected" # TODO: Implement this type

class Update(BaseModel):
    _id: UUID
    action: str
    type: UpdateType
    data: dict
    timestamp: int = time.time()

    class Config:
        orm_mode = True