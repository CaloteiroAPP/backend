
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pymongo.collection import Collection

from src.database.connection import db
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
    if not user_service.user_is_valid(user):
        return response_handler.bad_request(
            message="User is invalid",
        )
        
    # Create new user instance
    user = user_service.create_user(user)
    
    # Return the user instance with a success message
    create_user_response_dto = DTOUtils.user_to_create_user_response_dto(user)
    return response_handler.created(
        # data=user.model_dump(),
        data=create_user_response_dto.model_dump(),
        # data=create_user_response_dto,
        message="User created",
    )
