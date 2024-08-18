from typing import List, Optional
from uuid import UUID

from pymongo.collection import Collection

from src.models.expense_model import Expense
from src.repositories.repository_interface import RepositoryInterface


class ExpenseRepository(RepositoryInterface):
    def __init__(self, collection: Collection) -> None:
        super().__init__(collection)

    async def create_expense(self, expense: Expense) -> Expense:
        expense = await super().create(expense)
        return expense

    async def get_expense_by_id(self, expense_id: UUID) -> Optional[Expense]:
        expense_dict = await super().get_by_id(expense_id)
        if expense_dict:
            return Expense(**expense_dict)
        return None
    

