"""Contain Dish and User representations."""
from dataclasses import dataclass
from typing import Union

from aiogram import types
from aiogram.dispatcher.filters.state import StatesGroup, State

from dto_models import UserDTO, DishDTO


#
class FindDishState(StatesGroup):
    """State manager for aiogram final state machine."""

    enter_ingredients = State()
    show_dishes = State()
    show_instruction = State()
    history = State()
    show_history_dish = State()
    history_show_instruction = State()
    settings = State()
#
#
# class DishService:
#     def preview(self, dish_dto: DishDTO) -> str:
#         """Return str with dish title and ingredients."""
#         return dish_dto.title + '\n' + '\n' + dish_dto.ingredients
#
#
# class UserService:
#
#     def create_user(self, user_dto: UserDTO) -> None:
#
#         pass
#
#     def get_user_dishes(self, user_id: int) -> list[DishInBotRepr]:
#         """Return dishes in DB by user id."""
#
#     def get_user(self, user_id: int) -> Optional[TelegramUser]:
#         """Return user in DB, if user exist and None otherwise."""
#
#     def set_user_lang(self, user_id: int, lang: str) -> None:
#         """Return user in DB, if user exist and None otherwise."""
#
#     # def init_by_update(self, update: Union[types.Message, types.CallbackQuery]):
#     #     """
#     #     Init TelegramUser object by update.
#     #
#     #     :param update: aiogram object with input data
#     #     :return: TelegramUser
#     #     """
#     #     return UserDTO(
#     #         first_name=update.from_user.first_name,
#     #         last_name=update.from_user.last_name,
#     #         tg_id=update.from_user.id,
#     #         language="en",
#     #     )
