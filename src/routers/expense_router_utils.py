from src.dtos.create_expense_dto import CreateExpenseDTO
from src.models.expense_model import Expense
from src.models.expense_settings_model import ExpenseSettings


class ExpenseRouterUtils:

    @staticmethod
    def create_new_expense_from_create_expense_dto(expense: CreateExpenseDTO) -> Expense:
        expense_settings = ExpenseSettings(
            description=expense.description,
            method=expense.method,
            photo=expense.photo,
            type=expense.type,
        )

        return Expense(
            amount=expense.amount,
            currency=expense.currency,
            expense_settings=expense_settings,
            payer=expense.payer,
            session=expense.session,
            splitting=expense.splitting,
        )
