from src.dtos.create_expense_dto import CreateExpenseDTO
from src.models.expense_model import Expense
from src.repositories.expense_repository import ExpenseRepository
from src.services.service_interface import ServiceInterface


class ExpenseService(ServiceInterface):
    def __init__(self, expense_repository: ExpenseRepository):
        super().__init__(expense_repository)

    async def create_expense(self, expense: CreateExpenseDTO) -> Expense:
        # TODO: Add business logic here
        created_base_model = await super().create(expense)
        return Expense(** created_base_model.model_dump())

