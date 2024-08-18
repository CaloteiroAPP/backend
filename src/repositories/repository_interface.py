from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from pymongo.collection import Collection

class RepositoryInterface:
    def __init__(self, collection: Collection) -> None:
        self.collection = collection

    async def verify_id_is_available(self, resource_id: UUID) -> bool:
        return await self.collection.find_one({"_id": resource_id}) is None

    async def get_by_id(self, resource_id: UUID) -> Optional[dict]:
        return await self.collection.find_one({"_id": resource_id})

    async def create(self, resource: BaseModel) -> dict:
        if not self.verify_id_is_available(resource._id):
            raise ValueError(f"Resource with _id {resource._id} already exists")
        await self.collection.insert_one(resource.model_dump())
        return resource
