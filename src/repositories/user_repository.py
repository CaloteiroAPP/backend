

from typing import Collection, Optional
from uuid import UUID
from src.models.user_model import User
from src.repositories.repository_interface import RepositoryInterface


class UserRepository(RepositoryInterface):
    
    def __init__(self, collection: Collection) -> None:
        super().__init__(collection)
        
    def verify_id_is_available(self, user: User) -> bool:
        return super().verify_id_is_available(user)
    
    def get_by_id(self, user_id: UUID) -> Optional[dict]:
        return super().get_by_id(user_id)
    
    def create(self, user: User) -> User:
        user_base_model = super().create(user)
        return User(**user_base_model.model_dump())
    
    