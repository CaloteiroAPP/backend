from typing import List, Optional
from uuid import UUID

from src.models.expense_model import Expense, State
from src.repositories.expense_repository import ExpenseRepository
from src.services.service_interface import ServiceInterface


class ExpenseService(ServiceInterface):
    def __init__(self, expense_repository: ExpenseRepository):
        super().__init__(expense_repository)

    async def create_expense(self, expense: Expense) -> Expense:
        # TODO: Add business logic here
        return await super().create(expense)

