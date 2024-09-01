
import logging
from bson import ObjectId
from src.models.change_model import Change
from src.models.expense_model import Expense
from src.models.session_model import Session
from src.models.user_model import User
from src.repositories.session_repository import SessionRepository

_logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(name)s - %(message)s')


class SessionService:
    def __init__(self, session_repository: SessionRepository):
        self.repository = session_repository

    def get_session_by_id(self, session_id: ObjectId) -> Session | None:
        _logger.info(f"Getting session by id: {session_id}")
        session_base_model = self.repository.get_by_id(session_id)
        if session_base_model is None:
            return None
        return Session(**session_base_model)

    def verify_session_splitting(self, expense: Expense) -> tuple[bool, str]:
        _logger.info(f"Verifying session splitting: {expense.id}")

        # Verify the session exists
        session = self.get_session_by_id(expense.session)
        if session is None:
            return False, "Session does not exist"

        # Verify if payer has joined session
        if expense.payer_id not in session.members:
            return False, "Payer has no permission in session"

        # Verify if all the splitting users have joined session
        if not all([splitting.user_id in session.members for splitting in expense.splitting]):
            return False, "Splitting user has no permission in session"

        return True, "Session splitting is valid"
    
    def update_session(self, session: Session) -> None:
        _logger.info(f"Updating session: {session.id}")
        self.repository.update(session.id, session)
    
    def add_new_expense_to_session(self, expense: Expense, payer: User) -> None:
        _logger.info(f"Adding new expense to session: {expense.session}")
        
        # Get the session
        session = self.get_session_by_id(expense.session)
        
        # Add the expense to the session
        session.expenses.append(expense.id)

        # Add the change to the session
        _logger.info(f"Adding change to session: {expense.session}")
        session.activity.append(
            Change(change_message=f"{payer.full_name} added {expense.expense_settings.description}. {expense.amount}")
            )
        
        # Update the session
        self.update_session(session)
