from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from pymongo.collection import Collection


class RepositoryInterface:
    def __init__(self, collection: Collection) -> None:
        self.collection = collection

    def verify_id_is_available(self, resource: BaseModel) -> bool:
        return self.collection.find_one({"_id": resource.model_dump()}.get("_id")) is not None

    def get_by_id(self, resource_id: UUID) -> Optional[dict]:
        return self.collection.find_one({"_id": resource_id})

    def create(self, resource: BaseModel) -> BaseModel:
        self.collection.insert_one(resource.model_dump())
        return resource
