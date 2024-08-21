from uuid import uuid4
from src.models.expense_model import Expense
from src.repositories.expense_repository import ExpenseRepository


class ExpenseService:
    
    def __init__(self, expense_repository: ExpenseRepository):
        self.repository = expense_repository

    def create_expense(self, expense: Expense) -> Expense:
        while not self.repository.verify_expense_id_is_available(expense):
            expense = self.generate_new_id(expense)
        
        created_base_model = self.repository.create_expense(expense)
        return Expense(** created_base_model.model_dump())

    @staticmethod
    def generate_new_id(expense: Expense) -> Expense:
        expense_base_model = expense.model_dump()
        expense_base_model["_id"] = uuid4()
        return Expense(**expense_base_model)

    @staticmethod
    def expense_is_valid(expense: Expense) -> bool:
        # Amount is a negative number
        if expense.amount <= 0:
            return False
        # A splitting is less than 0
        elif any([splitting.amount < 0 for splitting in expense.splitting]):
            return False
        # The splittings exceed the amount
        elif sum([splitting.amount for splitting in expense.splitting]) != expense.amount:
            return False
        # The amount is not a valid float number for currency
        elif len(f"{float(expense.amount)}".split('.')[1]) <= 2:
            return False
        # A splitting is not a valid float number for currency
        elif any([len(f"{float(splitting.amount)}".split('.')[1]) <= 2]
                 for splitting in expense.splitting):
            return False

        return True
