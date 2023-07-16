"""Contain Dish and User representations."""
from dataclasses import dataclass
from typing import Union

from aiogram import types
from aiogram.dispatcher.filters.state import StatesGroup, State


class FindDishState(StatesGroup):
    """State manager for aiogram final state machine."""

    enter_ingredients = State()
    show_dishes = State()
    show_instruction = State()
    history = State()
    show_history_dish = State()
    history_show_instruction = State()
    settings = State()


@dataclass
class DishInBotRepr:  # stupid name
    """Representation of dish for bot."""

    title: str
    id: int
    image_url: str
    ingredients: str
    instruction: str = ""

    def preview(self) -> str:
        """Return str with dish title and ingredients."""
        return self.title + '\n' + '\n' + self.ingredients


@dataclass
class TelegramUser:
    """User model for TelegramBot."""

    tg_id: int
    first_name: str
    last_name: str
    language: str = "en"

    @staticmethod
    def init_by_update(update: Union[types.Message, types.CallbackQuery]):
        """
        Init TelegramUser object by update.

        :param update: aiogram object with input data
        :return: TelegramUser
        """
        return TelegramUser(
            first_name=update.from_user.first_name,
            last_name=update.from_user.last_name,
            tg_id=update.from_user.id,
            language="en",
        )
