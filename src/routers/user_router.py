from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pymongo.errors import DuplicateKeyError
from pymongo.collection import Collection

from src.database.connection import db
from src.dtos.create_friend_request import CreateFriendRequestDTO
from src.dtos.create_user_dto import CreateUserDTO
from src.dtos.dto_utils import DTOUtils
from src.models.user_model import User
from src.repositories.user_repository import UserRepository
from src.routers.response_handler import ResponseHandler
from src.services.user_service import UserService

user_collection: Collection = db["user"]
user_repository = UserRepository(user_collection)
user_service = UserService(user_repository)

response_handler = ResponseHandler()
router = APIRouter()


@router.post("/user/", response_model=User)
async def create_user(create_user_dto: CreateUserDTO
                      ) -> JSONResponse:
    # Create the user from the DTO
    user: User = DTOUtils.create_user_dto_to_user(create_user_dto)

    # Verify if the user is valid
    valid, message = user_service.user_is_valid(user)
    if not valid:
        return response_handler.bad_request(
            message=f"User is invalid. {message}",
        )
        
    # Verify if the user friend code
    user_service.verify_user_friend_code(user)

    # Create new user instance
    try: 
        user = user_service.create_user(user)
    except DuplicateKeyError:
        return response_handler.bad_request(
            message="User email already exists",
        )

    # Return the user instance with a success message
    create_user_response_dto = DTOUtils.user_to_create_user_response_dto(user)
    return response_handler.created(
        data=create_user_response_dto.model_dump(),
        message="User created",
    )


@router.post("/friend/", response_model=User)
async def create_friend_request(create_friend_request_dto: CreateFriendRequestDTO
                                ) -> JSONResponse:
    valid, message = user_service.friend_request_is_valid(create_friend_request_dto)
    if not valid:
        return response_handler.bad_request(
            message=f"Friend request is invalid. {message}",
        )

    user_service.add_friend_request(create_friend_request_dto)
    
    return response_handler.created(
        message="Friend request created",
    )
