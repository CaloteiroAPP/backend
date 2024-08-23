

from bson import ObjectId
from pymongo.collection import Collection

from src.models.session_model import Session
from src.repositories.repository_interface import RepositoryInterface


class SessionRepository(RepositoryInterface):
    
    def __init__(self, collection: Collection) -> None:
        super().__init__(collection)
        
    def verify_session_id_is_available(self, session: Session) -> bool:
        session_base_model = session.model_dump()
        return super().verify_id_is_available(session_base_model.get("id"))
    
    def get_session_by_id(self, session_id: ObjectId) -> dict | None:
        return super().get_by_id(session_id)
    
    def create_session(self, session: Session) -> Session:
        session_base_model = super().create(session)
        return Session(**session_base_model.model_dump())
