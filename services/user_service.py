from db import db_session
from db.repositories import DishRepository, UserRepository
from services.dto_models import UserDTO, DishDTO


# from .setup import dish_service


class UserService:
    def __init__(self, repository: UserRepository, dish_service):
        self.repository = repository
        self.dish_service = dish_service

    def get(self, idx: int):
        return self.repository.get(idx)

    def save(self, user: UserDTO):
        self.repository.save(user)

    def set_lang(self, user_id: int, lang: str):
        self.repository.set_lang(user_id, lang)

    def get_user_dishes(self, user_id: int) -> list[DishDTO]:
        dishes = self.repository.get_all_user_dishes(user_id)
        return self.dish_service.bound(dishes)

    def convert_dishes_list_to_str(self, dishes: list[DishDTO]) -> str:
        return self.dish_service.to_message_format(dishes)

    def add_user_to_dish_association(self, user: UserDTO, dish: DishDTO):
        self.repository.add_user_to_dish_association(user.tg_id, dish.id)
