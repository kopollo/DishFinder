"""Contain fsm group and keyboards."""
from dataclasses import dataclass

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

    def preview(self):
        return self.title + '\n' + '\n' + self.ingredients


@dataclass
class TelegramUser:
    tg_id: int
    first_name: str
    last_name: str
    language: str = "en"
