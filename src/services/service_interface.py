from pydantic import BaseModel

from src.repositories.repository_interface import RepositoryInterface


class ServiceInterface:
    def __init__(self, repository: RepositoryInterface) -> None:
        self.repository = repository

    async def create(self, expense: BaseModel) -> BaseModel:
        return await self.repository.create(expense)

