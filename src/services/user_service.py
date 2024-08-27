
import re

from bson import ObjectId

from src.dtos.create_friend_request import CreateFriendRequestDTO
from src.models.expense_model import Expense
from src.models.user_model import User
from src.models.user_settings_model import generate_user_friend_code
from src.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.repository = user_repository
        
    def get_user_by_id(self, user_id: ObjectId) -> User | None:
        user_base_model = self.repository.get_user_by_id(user_id)
        if user_base_model is None:
            return None
        return User(**user_base_model)
    
    def get_user_by_email(self, email: str) -> User | None:
        user_base_model = self.repository.get_user_by_email(email)
        if user_base_model is None:
            return None
        return User(**user_base_model)
        
    def verify_user_password(self, user_id: ObjectId, password: str) -> bool:
        user = self.get_user_by_id(user_id)
        if user is None or user.password != password:
            return False
        return True
    
    def verify_user_friend_code(self, user: User) -> User:
        while not self.repository.verify_user_friend_code_is_available(user):
            user.user_settings.friend_code = generate_user_friend_code()
        
        return user
    
    def verify_personal_splitting(self, expense: Expense) -> tuple[bool, str]:
        user = self.get_user_by_id(expense.payer)
        if user is None:
            return False, "User does not exist"
        elif not all([splitting.user in user.user_settings.friend_users for splitting in expense.splitting]):
            return False, "Not all the associated users in the splitting are friends with this user"
        return True, "All the associated users in the splitting are friends with this user"

    @staticmethod
    def user_is_valid(user: User) -> tuple[bool, str]:
        valid_email_patter = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
        if re.match(valid_email_patter, user.email) is None:
            return False, "Invalid email"
        elif len(user.password) < 3:
            return False, "Password is too short"
        elif len(user.first_name) < 2 or len(user.last_name) < 2 or len(user.first_name) > 20 or len(user.last_name) > 20:
            return False, "First name or last name is too short or too long"
        elif len(user.first_name.split()) > 1 or len(user.last_name.split()) > 1:
            return False, "First name or last name has spaces"
        elif not user.first_name.isalpha() or not user.last_name.isalpha():
            return False, "First name or last name has non-alphabetic characters"
        return True, "User is valid"

    def create_user(self, user: User) -> User:
        while not self.repository.verify_user_id_is_available(user):
            user = self.generate_new_id(user)
        return self.repository.create_user(user)

    @staticmethod
    def generate_new_id(user: User) -> User:
        user_base_model = user.model_dump()
        user_base_model["id"] = ObjectId()
        return User(**user_base_model)
    
    def friend_request_is_valid(self, create_friend_request_dto: CreateFriendRequestDTO) -> tuple[bool, str]:
        user = self.get_user_by_email(create_friend_request_dto.user_email)
        if user is None:
            return False, "User does not exist"
        friend = self.get_user_by_id(ObjectId(create_friend_request_dto.friend_id))
        if friend is None:
            return False, "Friend does not exist"

        if create_friend_request_dto.user_id == create_friend_request_dto.friend_id:
            return False, "Sender and receiver are the same"
        elif any(friend.id == friend_user.user for friend_user in user.user_settings.friend_users):
            return False, "Friend is already a friend"
        elif user.id in friend.user_settings.friend_requests:
            return False, "Friend request already exists"
        elif user.id in friend.user_settings.muted_users:
            return False, "User is muted by the friend"
        elif friend.id in user.user_settings.muted_users:
            return False, "Friend is muted by the user"
        return True, "Friend request is valid"
    
    def add_friend_request(self, create_friend_request_dto: CreateFriendRequestDTO) -> User:
        user = self.get_user_by_email(create_friend_request_dto.user_email)
        friend = self.get_user_by_id(ObjectId(create_friend_request_dto.friend_id))
        
        user.user_settings.friend_requests.append(friend.id)
        friend.user_settings.friend_requests.append(user.id)
        
        self.repository.update_user(user)
        self.repository.update_user(friend)