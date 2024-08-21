
from uuid import UUID

from src.models.expense_model import Expense
from src.models.user_model import User
from src.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.repository = user_repository
        
    def get_user_by_id(self, user_id: UUID) -> User | None:
        user_base_model = self.repository.get_by_id(user_id)
        if user_base_model is None:
            return None

        return User(**user_base_model)
        
    def verify_user_password(self, user_id: UUID, password: str) -> bool:
        user = self.get_user_by_id(user_id)        
        if user is None or user.password != password:
            return False
        
        return True

    def verify_personal_splitting(self, expense: Expense) -> bool:
        user = self.get_user_by_id(expense.payer)
        if user is None:
            return False

        if not all([splitting.user in user.user_settings.friend_users for splitting in expense.splitting]):
            return False

        return True
