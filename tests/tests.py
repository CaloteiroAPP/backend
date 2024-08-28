
    
# from src.dtos.create_user_dto import CreateUserDTO
# from src.dtos.dto_utils import DTOUtils
# from src.models.user_model import User


# create_user_dto = CreateUserDTO(
#     email="tiagogcarvalho2002@gmail.com",
#     first_name="Tiago",
#     last_name="Sora",
#     password="123456",
#     phone=123456789,
# )
# user: User = DTOUtils.create_user_dto_to_user(create_user_dto)

# print(user.model_dump())


a: float = 0.00

b: int = 0

print(a == b)


test = "multiple spaces   in between"

clean_test = " ".join(test.split())

print(clean_test)
