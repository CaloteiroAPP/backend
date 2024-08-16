from typing import List, Optional
from uuid import UUID

from repositories.expense_repository import ExpenseRepository
from src.models.expense import Expense, State


class ExpenseService:
    def __init__(self, expense_repository: ExpenseRepository):
        self.expense_repository = expense_repository

    def create_expense(self, expense: Expense) -> Expense:
        # TODO: Add business logic here if needed
        return self.expense_repository.create_expense(expense)

    def get_expense_by_id(self, expense_id: UUID) -> Optional[Expense]:
        return self.expense_repository.get_expense_by_id(expense_id)

    def update_expense(self, expense_id: UUID, updated_data: dict) -> Optional[Expense]:
        # TODO: Add business logic here if needed
        return self.expense_repository.update_expense(expense_id, updated_data)

    def delete_expense(self, expense_id: UUID) -> bool:
        return self.expense_repository.delete_expense(expense_id)

    def get_expenses_by_state(self, state: State) -> List[Expense]:
        return self.expense_repository.get_expenses_by_state(state)
