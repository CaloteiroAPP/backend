from uuid import UUID

from fastapi import APIRouter, Depends

from src.models.expense_model import Expense
from src.services.expense_service import ExpenseService

router = APIRouter()

@router.post("/expenses/", response_model=Expense)
async def create_expense(expense: Expense, service: ExpenseService = Depends(lambda: ExpenseService)) -> Expense:
    return await service.create_expense(expense)
