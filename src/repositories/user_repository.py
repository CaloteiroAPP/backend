

from functools import wraps
from bson import ObjectId
from pymongo.collection import Collection
from pymongo import errors
from src.models.user_model import User
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


class UserRepository(RepositoryInterface):
    
    def __init__(self, collection: Collection) -> None:
        super().__init__(collection)
        
    def verify_user_id_is_available(self, user: User) -> bool:
        user_base_model = user.model_dump()
        return super().verify_id_is_available(user_base_model.get("id"))
    
    def get_user_by_id(self, user_id: ObjectId) -> dict | None:
        return super().get_by_id(user_id)
    
    def get_user_by_email(self, email: str) -> dict | None:
        return self.collection.find_one({"email": email})
    
    def create_user(self, user: User) -> User:
        user_base_model = super().create(user)
        return User(**user_base_model.model_dump())
    
    def update_user(self, user: User) -> User:
        user_base_model = super().update(user.id, user)
        return User(**user_base_model.model_dump())
    
    def verify_user_friend_code_is_available(self, user: User) -> bool:
        return self.collection.find_one({"user_settings.friend_code": user.user_settings.friend_code}) is None
