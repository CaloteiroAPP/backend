from src.dtos.create_expense_dto import CreateExpenseDTO
from src.models.expense_model import Expense


def create_new_expense_from_create_expense_dto(expense: CreateExpenseDTO) -> Expense:
    return Expense(
        payer=expense.payer,
        amount=expense.amount,
        currency=expense.currency,
        description=expense.description,
        type=expense.type,
        spliting=expense.splitting,
    )
