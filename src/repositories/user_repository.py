

from bson import ObjectId
from pymongo.collection import Collection

from src.models.user_model import User
from src.repositories.repository_interface import RepositoryInterface


class UserRepository(RepositoryInterface):
    
    def __init__(self, collection: Collection) -> None:
        super().__init__(collection)
        
    def verify_user_id_is_available(self, user: User) -> bool:
        user_base_model = user.model_dump()
        return super().verify_id_is_available(user_base_model.get("id"))
    
    def get_user_by_id(self, user_id: ObjectId) -> dict | None:
        return super().get_by_id(user_id)
    
    def create_user(self, user: User) -> User:
        user_base_model = super().create(user)
        return User(**user_base_model.model_dump())
