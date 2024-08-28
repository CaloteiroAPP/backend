from bson import ObjectId
from pydantic import BaseModel
from pymongo.collection import Collection


class RepositoryInterface:
    def __init__(self, collection: Collection) -> None:
        self.collection = collection

    def verify_id_is_available(self, resource_id: ObjectId) -> bool:
        return self.collection.find_one({"id": resource_id}) is None

    def get_by_id(self, resource_id: ObjectId) -> dict | None:
        return self.collection.find_one({"id": resource_id})

    def create(self, resource: BaseModel) -> BaseModel:
        self.collection.insert_one(resource.model_dump())
        return resource
    
    def update(self, resource_id: ObjectId, resource: BaseModel) -> BaseModel:
        self.collection.update_one({"id": resource_id}, {"$set": resource.model_dump()})
        return resource
