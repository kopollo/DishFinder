"""Contain Dish and User representations."""

from aiogram.dispatcher.filters.state import StatesGroup, State


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
