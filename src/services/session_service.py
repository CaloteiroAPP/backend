from uuid import UUID

from src.models.expense_model import Expense
from src.models.session_model import Session
from src.repositories.session_repository import SessionRepository


class SessionService:
    def __init__(self, session_repository: SessionRepository):
        self.repository = session_repository

    def get_session_by_id(self, session_id: UUID) -> Session | None:
        session_base_model = self.repository.get_by_id(session_id)
        if session_base_model is None:
            return None
        return Session(**session_base_model)

    def verify_session_splitting(self, expense: Expense) -> bool:

        # Verify the session exists
        session = self.get_session_by_id(expense.session_id)
        if session is None:
            return False

        # Verify if payer has joined session
        if expense.payer not in session.members:
            return False

        # Verify if all the splitting users have joined session
        if not all([splitting.user in session.members for splitting in expense.splitting]):
            return False

        return True

