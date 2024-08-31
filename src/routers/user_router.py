from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pymongo.errors import DuplicateKeyError
from pymongo.collection import Collection

from src.database.connection import db
from src.dtos.create_friend_request import CreateFriendRequestDTO
from src.dtos.create_user_dto import CreateUserDTO
from src.dtos.dto_utils import DTOUtils
from src.models.friend_request_model import FriendRequest
from src.models.user_model import User
from src.repositories.user_repository import UserRepository
from src.routers.response_handler import ResponseHandler
from src.services.user_service import UserService

_user_collection: Collection = db["user"]
_user_repository = UserRepository(_user_collection)
_user_service = UserService(_user_repository)

_response_handler = ResponseHandler()
router = APIRouter()


@router.post("/user/", response_model=User)
async def create_user(create_user_dto: CreateUserDTO
                      ) -> JSONResponse:
    # Create the user from the DTO
    user: User = DTOUtils.create_user_dto_to_user(create_user_dto)

    # Verify if the user is valid
    valid, message = _user_service.user_is_valid(user)
    if not valid:
        return _response_handler.bad_request(
            message=f"User is invalid. {message}",
        )

    # Verify if the user friend code
    _user_service.verify_user_friend_code(user)

    # Create new user instance
    try:
        user = _user_service.create_user(user)
    except DuplicateKeyError:
        return _response_handler.bad_request(
            message="User email already exists",
        )

    # Return the user instance with a success message
    create_user_response_dto = DTOUtils.user_to_create_user_response_dto(user)
    return _response_handler.created(
        data=create_user_response_dto.model_dump(),
        message="User created",
    )


@router.post("/friend/", response_model=User)
async def create_friend_request(create_friend_request_dto: CreateFriendRequestDTO
                                ) -> JSONResponse:
    # Verify if the payer password is correct
    if not _user_service.verify_user_id_password(create_friend_request_dto.user_id,
                                                 create_friend_request_dto.user_password):
        return _response_handler.unauthorized(
            message="Unauthorized access",
        )

    # Verify if the friend request is valid
    valid, message, _ = _user_service.friend_request_is_valid(create_friend_request_dto)
    if not valid:
        return _response_handler.bad_request(
            message=f"Friend request is invalid. {message}",
        )

    # Create new friend request instance
    _user_service.add_friend_request(
        FriendRequest(user=create_friend_request_dto.user_id, friend=create_friend_request_dto.friend_id)
        )

    # Return the friend request instance with a success message
    return _response_handler.created(
        message="Friend request created",
    )
