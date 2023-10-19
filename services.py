from typing import Optional

from db import DishModel, db_session
from db.repositories import DishRepository, UserRepository
from dto_models import *


class DishService:
    def __init__(self, repository: DishRepository):
        self.repository = repository

    def get(self, idx: int):
        return self.repository.get(idx)

    def save(self, dish: DishDTO):
        self.repository.save(dish)

    @staticmethod
    def bound(dishes: list[DishDTO]) -> list[DishDTO]:
        """Limit the number of dishes shown to the user to 10."""
        return dishes[:10]

    @staticmethod
    def to_message_format(dishes: list[DishDTO]) -> str:
        """
        Format dishes for bot message to show user.

        :param dishes: list of dishes
        :return: str
        """
        ans = ''
        for i, dish in enumerate(dishes):
            ans += f'{i}) {dish.title}\n'
        return ans

    def get_formatted_dishes(self, dishes: list[DishDTO]):
        # user_repository.get_all_user_dishes(user_id)
        return self.to_message_format(self.bound(dishes))


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get(self, idx: int):
        return self.repository.get(idx)

    def save(self, user: UserDTO):
        self.repository.save(user)

    def set_lang(self, user_id: int, lang: str):
        self.repository.set_lang(user_id, lang)

    def get_user_dishes(self, user_id: int) -> list[DishDTO]:
        dishes = self.repository.get_all_user_dishes(user_id)
        return dish_service.bound(dishes)

    @staticmethod
    def convert_dishes_list_to_str(dishes: list[DishDTO]) -> str:
        return dish_service.to_message_format(dishes)

    def add_user_to_dish_association(self, user: UserDTO, dish: DishDTO):
        self.repository.add_user_to_dish_association(user.tg_id, dish.id)


s = db_session.create_session()
dish_service = DishService(DishRepository(s))
user_service = UserService(UserRepository(s))

# class DBService:
#     def __init__(self):
#         self.dish_repository: DishRepository = DishRepository()
#         self.user_repository: UserRepository = UserRepository()
#
#     def save_dish_to_user_event(self, dish: DishDTO, user: UserDTO):
#         self.dish_repository.save(dish)
#         self.user_repository.add_user_to_dish_association(
#             dish_id=dish.id,
#             user_id=user.tg_id,
#         )
# def save_dish(self, dish: DishDTO) -> None:
#     dish_repository.add(dish)
#
# # dish_repository.save(dish)
#
# def get_dish(self, dish_id: int) -> DishDTO:
#     dish = dish_repository.get(dish_id)
#     return dish
#
# #
# # def init_dishes_by_api(self, ingredients) -> list[DishDTO]:
# #     manager = FoodApiManager(ingredients)
# #     return manager.get_dishes()
#
# def get_all_user_dishes(self, user_id: int) -> list[DishDTO]:
#     """Return dishes in DB by user id."""
#     dishes = get_all_user_dishes(user_id)
#     # dishes = [self._to_dish_in_bot_repr(i) for i in dishes]
#     return dishes
#
# def add_user(self, user: UserDTO) -> None:
#     """Add user to DB."""
#     user_repository.save(user)
#
# def get_user(self, user_id) -> Optional[UserDTO]:
#     """Return user in DB, if user exist and None otherwise."""
#     user: UserDTO = user_repository.get(user_id)
#     if not user:
#         return None
#     return user
#
# def set_user_lang(self, user_id: int, lang: str) -> None:
#     """
#     Set user lang.
#     :param user_id:
#     :param lang:
#     :return:
#     """
#     try:
#         user_repository.set_lang(user_id=user_id, lang=lang)
#     except Exception:
#         print('cant set lang to user')
