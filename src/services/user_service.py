
import re

from bson import ObjectId

from src.models.expense_model import Expense
from src.models.user_model import User
from src.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.repository = user_repository
        
    def get_user_by_id(self, user_id: ObjectId) -> User | None:
        user_base_model = self.repository.get_by_id(user_id)
        if user_base_model is None:
            return None

        return User(**user_base_model)
        
    def verify_user_password(self, user_id: ObjectId, password: str) -> bool:
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

    @staticmethod
    def user_is_valid(user: User) -> bool:
        valid_email_patter = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
        if re.match(valid_email_patter, user.email) is None:
            return False
        elif len(user.password) < 3:
            return False
        elif len(user.first_name) < 2 or len(user.last_name) < 2:
            return False
        elif not user.first_name.isalpha() or not user.last_name.isalpha():
            return False
        return True

    def create_user(self, user: User) -> User:
        print("Verifying user")
        while not self.repository.verify_user_id_is_available(user):
            user = self.generate_new_id(user)
            
        print("Creating user")
        return self.repository.create_user(user)

    @staticmethod
    def generate_new_id(user: User) -> User:
        print("Generating new id")
        user_base_model = user.model_dump()
        user_base_model["id"] = ObjectId()
        return User(**user_base_model)
