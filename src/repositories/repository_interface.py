from functools import wraps
from bson import ObjectId
from pydantic import BaseModel
from pymongo import errors
from pymongo.collection import Collection


def handle_db_error(func):
    """Decorator to handle MongoDB related errors."""

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except errors.PyMongoError:
            return None

    return wrapper


class RepositoryInterface:
    def __init__(self, collection: Collection) -> None:
        self.collection = collection

    @handle_db_error
    def verify_id_is_available(self, resource_id: ObjectId) -> bool:
        return self.collection.count_documents({"id": resource_id}) == 0

    @handle_db_error
    def get_by_id(self, resource_id: ObjectId) -> dict | None:
        return self.collection.find_one({"id": resource_id})

    @handle_db_error
    def create(self, resource: BaseModel) -> BaseModel | None:
        self.collection.insert_one(resource.dict())
        return resource

    @handle_db_error
    def update(self, resource_id: ObjectId, resource: BaseModel) -> BaseModel | None:
        result = self.collection.update_one(
            {"_id": resource_id},
            {"$set": resource.dict()},
            upsert=False
        )
        if result.matched_count == 0:
            return None
        return resource
