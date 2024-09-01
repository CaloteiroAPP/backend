import re

from bson import ObjectId

from src.dtos.create_friend_request import CreateFriendRequestDTO
from src.models.expense_model import Expense
from src.models.friend_model import Friend
from src.models.friend_request_model import FriendRequest
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

    def get_user_by_email(self, user_email: str) -> User | None:
        user_base_model = self.repository.get_user_by_email(user_email)
        if user_base_model is None:
            return None
        return User(**user_base_model)

    def verify_user_id_password(self, user_id: str, password: str) -> bool:
        user = self.get_user_by_id(ObjectId(user_id))
        if user is None or user.password != password:
            return False
        return True

    def verify_user_friend_code(self, user: User) -> User:
        while not self.repository.verify_user_friend_code_is_available(user):
            user.user_settings.friend_code = generate_user_friend_code()

        return user

    def verify_personal_splitting(self, expense: Expense) -> tuple[bool, str]:
        user = self.get_user_by_id(expense.payer_id)
        if user is None:
            return False, "User does not exist"
        elif not all([splitting.user_id in user.user_settings.friend_users for splitting in expense.splitting]):
            return False, "Not all the associated users in the splitting are friends with this user"
        return True, "All the associated users in the splitting are friends with this user"

    @staticmethod
    def user_is_valid(user: User) -> tuple[bool, str]:
        valid_email_patter = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
        if re.match(valid_email_patter, user.email) is None:
            return False, "Invalid email"
        elif len(user.password) < 3:
            return False, "Password is too short"
        elif len(user.first_name) < 2 or len(user.last_name) < 2 or len(user.first_name) > 20 or len(
                user.last_name) > 20:
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

    def verify_general_errors_in_friend_request(self, friend_request_dto: CreateFriendRequestDTO
                                                ) -> tuple[bool, str, User | None, User | None]:
        if friend_request_dto.user_id == friend_request_dto.friend_id:
            return False, "Sender and receiver are the same", None, None

        user = self.get_user_by_id(ObjectId(friend_request_dto.user_id))
        if user is None:
            return False, "User does not exist", None, None
        friend = self.get_user_by_id(ObjectId(friend_request_dto.friend_id))
        if friend is None:
            return False, "Friend does not exist", None, None

        if any(friend.id == friend_user.user_id for friend_user in user.user_settings.friend_users):
            return False, "Friend is already a friend", None, None
        elif user.id in friend.user_settings.muted_users:
            return False, "User is muted by the friend", None, None
        elif friend.id in user.user_settings.muted_users:
            return False, "Friend is muted by the user", None, None

        return True, "No general errors", user, friend

    def friend_request_is_valid(self, create_friend_request_dto: CreateFriendRequestDTO
                                ) -> tuple[bool, str, FriendRequest | None]:
        valid, message, user, friend = self.verify_general_errors_in_friend_request(create_friend_request_dto)
        if not valid:
            return False, message, None

        if user.id in friend.user_settings.friend_requests:
            return False, "Friend request already exists", None

        return True, "Friend request is valid", FriendRequest(user=user, friend=friend)

    def friend_request_acceptance_is_valid(self, accept_friend_request_dto: CreateFriendRequestDTO
                                           ) -> tuple[bool, str, FriendRequest | None]:
        valid, message, user, friend = self.verify_general_errors_in_friend_request(accept_friend_request_dto)
        if not valid:
            return False, message, None

        if friend.id not in user.user_settings.friend_requests:
            return False, "Friend request does not exist", None

        return True, "Friend request acceptance is valid", FriendRequest(user=user, friend=friend)

    def add_friend_request(self, friend_request: FriendRequest) -> bool:
        user = friend_request.user
        friend = friend_request.friend

        friend.user_settings.friend_requests.append(user.id)

        if self.repository.update_user(friend) is None:
            return False
        return True

    def add_friend(self, friend_request: FriendRequest) -> bool:
        user = friend_request.user
        friend = friend_request.friend

        user.user_settings.friend_users.append(Friend(user_id=friend.id))
        friend.user_settings.friend_users.append(Friend(user_id=user.id))

        user.user_settings.friend_requests.remove(friend.id)
        
        if self.repository.update_user(user) is None or self.repository.update_user(friend) is None:
            return False
        return True
