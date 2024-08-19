from fastapi import APIRouter, Depends

from src.dtos.create_expense_dto import CreateExpenseDTO
from src.models.expense_model import Expense
from src.services.expense_service import ExpenseService

router = APIRouter()

@router.post("/expenses/", response_model=Expense)
async def create_expense(expense: CreateExpenseDTO,
                         service: ExpenseService = Depends(lambda: ExpenseService)
                         ) -> Expense:
    
    print("Valid expense")
    
    # Example mock response that matches the `Expense` model
    expense = Expense(
        payer=expense.payer,
        amount=expense.amount,
        currency=expense.currency,
        description=expense.description,
        type=expense.type,
        splitting=expense.splitting
    )
    print(expense.model_dump())
    return expense
    # return await service.create_expense(expense)
