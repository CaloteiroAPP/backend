from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pymongo.collection import Collection

from src.database.connection import db
from src.dtos.create_expense_dto import CreateExpenseDTO
from src.dtos.dto_utils import DTOUtils
from src.models.expense_model import Expense
from src.repositories.expense_repository import ExpenseRepository
from src.repositories.session_repository import SessionRepository
from src.repositories.user_repository import UserRepository
from src.routers.response_handler import ResponseHandler
from src.services.expense_service import ExpenseService
from src.services.session_service import SessionService
from src.services.user_service import UserService

expense_collection: Collection = db["expense"]
expense_repository = ExpenseRepository(expense_collection)
expense_service = ExpenseService(expense_repository)

session_collection: Collection = db["session"]
session_repository = SessionRepository(session_collection)
session_service = SessionService(session_repository)

user_collection: Collection = db["user"]
user_repository = UserRepository(user_collection)
user_service = UserService(user_repository)

response_handler = ResponseHandler()
router = APIRouter()


@router.post("/expense/", response_model=Expense)
async def create_expense(create_expense_dto: CreateExpenseDTO,
                         ) -> JSONResponse:
    # Create the expense from the DTO
    expense = DTOUtils.create_expense_dto_to_expense(create_expense_dto)
    
    # Verify if the payer password is correct
    if not user_service.verify_user_password(expense.payer, create_expense_dto.payer_password):
        return response_handler.unauthorized(
            message="Unauthorized access",
        )

    # Verify if the expense is valid
    valid, message = expense_service.expense_is_valid(expense)
    if not valid:
        return response_handler.bad_request(
            message=f"Expense is invalid. {message}",
        )

    # Verify if the user has access inside the session
    if expense.session is not None:
        if not session_service.verify_session_splitting(expense):
            return response_handler.bad_request(
                message="Actions are not allowed in this session",
            )
    # Verify if all the associated users in the splitting are friends with this user
    elif not user_service.verify_personal_splitting(expense):
        return response_handler.bad_request(
            message="Actions are not allowed in this user",
        )

    # Create new expense instance
    # expense = expense_service.create_expense(expense)
    
    # Add activity to the session
    if expense.session is not None:
        session_service.add_activity(expense)  # TODO: Implement this method

    create_expense_response = DTOUtils.expense_to_create_expense_response_dto(expense)
    # Return the expense instance with a success message
    return response_handler.created(
        data=create_expense_response.model_dump(),
        message="Expense created",
    )
