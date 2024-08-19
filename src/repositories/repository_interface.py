from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from pymongo.collection import Collection


class RepositoryInterface:
    def __init__(self, collection: Collection) -> None:
        self.collection = collection

    async def verify_id_is_available(self, resource: BaseModel) -> bool:
        return await self.collection.find_one({"_id": resource.model_dump()}.get("_id")) is None

    async def get_by_id(self, resource_id: UUID) -> Optional[dict]:
        return await self.collection.find_one({"_id": resource_id})

    async def create(self, resource: BaseModel) -> BaseModel:
        if not self.verify_id_is_available(resource):
            raise ValueError(f"Resource already exists")
        self.collection.insert_one(resource.model_dump())
        return resource
