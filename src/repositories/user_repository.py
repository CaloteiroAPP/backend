

from typing import Collection
from src.repositories.repository_interface import RepositoryInterface


class UserRepository(RepositoryInterface):
    
    def __init__(self, collection: Collection) -> None:
        super().__init__(collection)
        
    def validate_user(self, username: str, password: str):
        return self.collection.find_one({"_private_key": username, "password": password})