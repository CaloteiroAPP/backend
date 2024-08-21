from fastapi import APIRouter, Depends

from src.dtos.create_expense_dto import CreateExpenseDTO
from src.models.expense_model import Expense
from src.routers.expense_router_utils import ExpenseRouterUtils
from src.routers.response_handler import ResponseHandler
from src.services.expense_service import ExpenseService
from src.services.session_service import SessionService
from src.services.user_service import UserService
from fastapi.responses import JSONResponse

response_handler = ResponseHandler()
router = APIRouter()


@router.post("/expense/", response_model=Expense)
async def create_expense(expense_dto: CreateExpenseDTO,
                         expense_service: ExpenseService = Depends(lambda: ExpenseService),
                         session_service: SessionService = Depends(lambda: SessionService),
                         user_service: UserService = Depends(lambda: UserService)
                         ) -> JSONResponse:
    # Verify if the payer password is correct
    if not user_service.verify_user_password(expense_dto.payer, expense_dto.payer_password):
        return response_handler.unauthorized(
            message="Unauthorized access",
        )

    # Create the expense
    expense: Expense = ExpenseRouterUtils.create_new_expense_from_create_expense_dto(expense_dto)

    # Verify if the expense is valid
    if not expense_service.expense_is_valid(expense):
        return response_handler.bad_request(
            message="Expense is invalid",
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
    expense = expense_service.create_expense(expense)

    return response_handler.created(
        data=expense.to_dict(),
        message="Expense created",
    )
