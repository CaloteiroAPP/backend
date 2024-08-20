

from typing import Collection
from src.repositories.repository_interface import RepositoryInterface


class NotificationRepository(RepositoryInterface):
    
    def __init__(self, collection: Collection) -> None:
        super().__init__(collection)
        