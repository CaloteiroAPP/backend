from typing import List, Optional
from uuid import UUID

from pymongo.collection import Collection

from src.models.expense import Expense, State


class ExpenseRepository:
    def __init__(self, collection: Collection):
        self.collection = collection

    def create_expense(self, expense: Expense) -> Expense:
        expense_dict = expense.dict()
        self.collection.insert_one(expense_dict)
        return expense

    def get_expense_by_id(self, expense_id: UUID) -> Optional[Expense]:
        expense_dict = self.collection.find_one({"_id": expense_id})
        if expense_dict:
            return Expense(**expense_dict)
        return None

    def update_expense(self, expense_id: UUID, updated_data: dict) -> Optional[Expense]:
        result = self.collection.update_one({"_id": expense_id}, {"$set": updated_data})
        if result.modified_count > 0:
            return self.get_expense_by_id(expense_id)
        return None

    def delete_expense(self, expense_id: UUID) -> bool:
        result = self.collection.delete_one({"_id": expense_id})
        return result.deleted_count > 0

    def get_expenses_by_state(self, state: State) -> List[Expense]:
        expenses = self.collection.find({"state": state.value})
        return [Expense(**exp) for exp in expenses]
