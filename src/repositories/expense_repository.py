
from functools import wraps
from bson import ObjectId
from pymongo.collection import Collection
from pymongo import errors
from src.models.expense_model import Expense
from src.repositories.repository_interface import RepositoryInterface


def handle_db_error(func):
    """Decorator to handle MongoDB related errors."""

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except errors.PyMongoError:
            return None

    return wrapper


class ExpenseRepository(RepositoryInterface):
    
    # SUPERCLASS METHODS IMPLEMENTATION
    
    def __init__(self, collection: Collection) -> None:
        super().__init__(collection)

    def verify_expense_id_is_available(self, expense: Expense) -> bool:
        expense_base_model = expense.model_dump()
        return super().verify_id_is_available(expense_base_model.get("id"))
    
    def create_expense(self, expense: Expense) -> Expense:
        created_base_model = super().create(expense)
        expense = Expense(**created_base_model.model_dump())
        return expense

    def get_expense_by_id(self, expense_id: ObjectId) -> Expense | None:
        expense_base_model = super().get_by_id(expense_id)
        if expense_base_model:
            return Expense(**expense_base_model)
        return None
    
    # CLASS METHODS
    
    

