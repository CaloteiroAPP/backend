import logging
from bson import ObjectId
from src.dtos.create_expense_dto import CreateExpenseDTO
from src.dtos.create_user_dto import CreateUserDTO
from src.dtos.create_user_response_dto import CreateUserResponseDTO
from src.models.expense_model import Expense
from src.models.expense_settings_model import ExpenseSettings
from src.models.splitting_model import Splitting
from src.models.user_model import User
from src.models.user_settings_model import UserSettings

_logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(name)s - %(message)s')


class DTOUtils:

    @staticmethod
    def create_expense_dto_to_expense(create_expense_dto: CreateExpenseDTO) -> Expense:

        _logger.info("Creating Expense from CreateExpenseDTO")

        expense_settings = ExpenseSettings(
            description=" ".join(create_expense_dto.description.split()),
            method=create_expense_dto.method,
            photo=create_expense_dto.photo,
            type=create_expense_dto.type,
        )
        
        splitting = [
            Splitting(amount=splitting.amount, settings=splitting.settings, user_id=ObjectId(splitting.user_id))
            for splitting in create_expense_dto.splitting
        ]

        return Expense(
            amount=create_expense_dto.amount,
            currency=create_expense_dto.currency,
            expense_settings=expense_settings,
            payer_id=ObjectId(create_expense_dto.payer_id),
            session=create_expense_dto.session,
            splitting=splitting,
        )

    @staticmethod
    def create_user_dto_to_user(create_user_dto: CreateUserDTO) -> User:
        
        _logger.info("Creating User from CreateUserDTO")
        
        user_settings = UserSettings(
            phone=create_user_dto.phone,
            photo=create_user_dto.photo,
        )
        
        return User(
            email=create_user_dto.email,
            first_name=create_user_dto.first_name,
            last_name=create_user_dto.last_name,
            full_name=create_user_dto.first_name + " " + create_user_dto.last_name,
            password=create_user_dto.password,
            user_settings=user_settings,
        )

    @classmethod
    def user_to_create_user_response_dto(cls, user: User) -> CreateUserResponseDTO:
        
        _logger.info("Creating CreateUserResponseDTO from User")
        
        return CreateUserResponseDTO(
            id=str(user.id),
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            full_name=user.full_name,
            password=user.password,
            user_settings=user.user_settings,
        )
        
    @staticmethod
    def expense_to_create_expense_response_dto(expense: Expense) -> CreateExpenseDTO:
        
        _logger.info("Creating CreateExpenseDTO from expense")
        
        expense_settings = ExpenseSettings(
            description=" ".join(expense.expense_settings.description.split()),
            method=expense.expense_settings.method,
            photo=expense.expense_settings.photo,
            type=expense.expense_settings.type,
        )

        return CreateExpenseDTO(
            id=str(expense.id),
            amount=expense.amount,
            currency=expense.currency,
            expense_settings=expense_settings,
            payer=expense.payer_id,
            session=expense.session,
            splitting=expense.splitting,
            state=expense.state,
            timestamp=expense.timestamp,
        )
