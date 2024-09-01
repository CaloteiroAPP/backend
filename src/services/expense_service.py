from uuid import uuid4
from src.models.expense_model import Expense
from src.models.expense_settings_model import SplittingMethod
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
        expense_base_model["id"] = uuid4()
        return Expense(**expense_base_model)

    @staticmethod
    def expense_is_valid(expense: Expense) -> tuple[bool, str]:
        
        # Amount is a negative number
        if expense.amount <= 0:
            return False, "Amount is a negative number"
        # A splitting is less than 0
        elif any([splitting.amount < 0 for splitting in expense.splitting]):
            return False, "A splitting is less than 0"
        # The splittings exceed the amount
        elif sum([splitting.amount for splitting in expense.splitting]) != expense.amount:
            return False, "The splittings exceed the amount"
        # The amount is not a valid float number for currency
        elif len(f"{float(expense.amount)}".split('.')[1]) > 2:
            return False, "The amount is not a valid float number for currency"
        # A splitting is not a valid float number for currency
        elif any([len(f"{float(splitting.amount)}".split('.')[1]) > 2
                  for splitting in expense.splitting]):
            return False, "A splitting is not a valid float number for currency"
        # The payer is not in the splittings
        elif expense.payer_id not in [splitting.user_id for splitting in expense.splitting]:
            return False, "The payer is not in the splittings"
        # A splitting user is duplicated
        elif len(set([splitting.user_id for splitting in expense.splitting])) != len(expense.splitting):
            return False, "A splitting user is duplicated"
        # The method is not valid
        elif expense.expense_settings.method not in SplittingMethod:
            return False, "The method is not valid"
        elif expense.expense_settings.method == SplittingMethod.EQUAL_SPLITTING:
            # All the splittings are not equal
            if len(set([splitting.amount for splitting in expense.splitting])) != 1:
                return False, "All the splittings are not equal in equal splitting"
        elif expense.expense_settings.method == SplittingMethod.I_PAY_ALL:
            # The payer is not the one who pays all
            if any([splitting.amount != 0 for splitting in expense.splitting if splitting.user_id != expense.payer_id]):
                return False, "The payer is not the one who pays all in I pay all"
        elif expense.expense_settings.method == SplittingMethod.YOU_PAY_ALL:
            # The payer is not the one who is owned all
            if any([splitting.amount != 0 for splitting in expense.splitting if splitting.user_id == expense.payer_id]):
                return False, "The payer is not the one who is owned all in you pay all"
        
        return True, "Expense is valid"
