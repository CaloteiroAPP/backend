
from typing import Collection, Optional
from uuid import UUID

from src.models.session_model import Session
from src.repositories.repository_interface import RepositoryInterface


class SessionRepository(RepositoryInterface):
    
    def __init__(self, collection: Collection) -> None:
        super().__init__(collection)
        
    def verify_id_is_available(self, session: Session) -> bool:
        return super().verify_id_is_available(session)
    
    def get_by_id(self, session_id: UUID) -> Optional[dict]:
        return super().get_by_id(session_id)
    
    def create(self, session: Session) -> Session:
        session_base_model = super().create(session)
        return Session(**session_base_model.model_dump())
