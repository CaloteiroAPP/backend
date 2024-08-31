from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pymongo.collection import Collection

from src.database.connection import db
from src.dtos.create_expense_dto import CreateExpenseDTO
from src.dtos.dto_utils import DTOUtils
from src.models.expense_model import Expense
from src.models.notification_model import NotificationType
from src.repositories.expense_repository import ExpenseRepository
from src.repositories.notification_repository import NotificationRepository
from src.repositories.session_repository import SessionRepository
from src.repositories.user_repository import UserRepository
from src.routers.response_handler import ResponseHandler
from src.services.cache_service import CacheService
from src.services.expense_service import ExpenseService
from src.services.notification_service import NotificationService
from src.services.session_service import SessionService
from src.services.user_service import UserService

_expense_collection: Collection = db["expense"]
_expense_repository = ExpenseRepository(_expense_collection)
_expense_service = ExpenseService(_expense_repository)

_notification_collection: Collection = db["notification"]
_notification_repository = NotificationRepository(_notification_collection)
_notification_service = NotificationService(_notification_repository)

_session_collection: Collection = db["session"]
_session_repository = SessionRepository(_session_collection)
_session_service = SessionService(_session_repository)

_user_collection: Collection = db["user"]
_user_repository = UserRepository(_user_collection)
_user_service = UserService(_user_repository)

_response_handler = ResponseHandler()
router = APIRouter()

_cache_service = CacheService()


@router.post("/expense/", response_model=Expense)
async def create_expense(create_expense_dto: CreateExpenseDTO,
                         ) -> JSONResponse:
    # Verify if the payer password is correct
    cached_valid: bool | None = _cache_service.get_or_set(
        str({"user_service_verify_user_password": (create_expense_dto.payer_id, create_expense_dto.payer_password)}),
        lambda: _user_service.verify_user_id_password(create_expense_dto.payer_id, create_expense_dto.payer_password)
    )
    # If the cached result (or newly computed one) is False, deny access
    if not cached_valid:
        return _response_handler.unauthorized(
            message="Unauthorized access",
        )
        
    # Create the expense from the DTO
    expense = DTOUtils.create_expense_dto_to_expense(create_expense_dto)
    payer = _user_service.get_user_by_id(expense.payer_id)

    # Verify if the expense is valid
    valid, message = _expense_service.expense_is_valid(expense)
    if not valid:
        return _response_handler.bad_request(
            message=f"Expense is invalid. {message}",
        )

    # Verify if the user has access inside the session
    if expense.session is not None:
        valid, message = _session_service.verify_session_splitting(expense)
        if not valid:
            return _response_handler.bad_request(
                message=f"Actions are not allowed in this session. {message}",
            )
    # Verify if all the associated users in the splitting are friends with this user
    else:
        valid, message = _user_service.verify_personal_splitting(expense)
        if not valid:
            return _response_handler.bad_request(
                message=f"Actions are not allowed for this user. {message}",
            )

    # Create new expense instance
    expense = _expense_service.create_expense(expense)
    
    # Add activity to the session
    if expense.session is not None:
        _session_service.add_new_expense_to_session(expense, payer)
        
    # Notify the users that are associated with the expense
    notifications_list = _notification_service.create_notifications_list(
        users=[splitting.user_id for splitting in expense.splitting],
        n_type=NotificationType.EXPENSE_ADDED,
        session=expense.session,
        data={"expense_id": expense.id, "amount": expense.amount,
              "description": expense.expense_settings.description, "payer": payer.id},
    )
    _notification_service.create_notifications(notifications_list)

    create_expense_response = DTOUtils.expense_to_create_expense_response_dto(expense)
    # Return the expense instance with a success message
    return _response_handler.created(
        data=create_expense_response.model_dump(),
        message="Expense created",
    )
