"""Contain fsm group and keyboards."""
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, \
    KeyboardButton, InlineKeyboardButton

from db import DishModel


class FindDishState(StatesGroup):
    """State manager for aiogram fsm."""

    enter_ingredients = State()
    show_dishes = State()
    more_info = State()
    history = State()


class StartKeyboard:
    """Keyboard for start state."""

    start_kb = ReplyKeyboardMarkup(resize_keyboard=True,
                                   one_time_keyboard=True)
    find_dish_btn = KeyboardButton(
        text='/find_dish',
    )
    history_btn = KeyboardButton('/history')
    start_kb.add(find_dish_btn, history_btn)


class ChooseDishKeyboard:
    """keyboard for dishes pagination for show_dishes state."""

    choose_kb = InlineKeyboardMarkup(row_width=3)
    back_btn = InlineKeyboardButton(
        text='prev',
        callback_data='prev'
    )
    next_btn = InlineKeyboardButton(
        text='next',
        callback_data='next',
    )
    stop_btn = InlineKeyboardButton(
        text='stop',
        callback_data='stop',
    )
    more_btn = InlineKeyboardButton(
        text='more',
        callback_data='more',
    )
    choose_kb.add(back_btn, more_btn, next_btn, stop_btn)


class MoreInfoKeyboard:
    """keyboard for more_info state."""

    more_kb = InlineKeyboardMarkup()
    back_btn = InlineKeyboardButton(
        text='back',
        callback_data='back'
    )
    save_btn = InlineKeyboardButton(
        text='save recipe',
        callback_data='save',
    )
    more_kb.add(back_btn, save_btn)


class HistoryKeyboard:
    """Autogenerated Keyboard for user history state."""

    @staticmethod
    def generate_kb(dishes: list[DishModel]) -> InlineKeyboardMarkup:
        """
        Generate keyboard by list of DishModel with callback view as dish_{id}.

        :param dishes: list[DishModel]
        :return: InlineKeyboardMarkup
        """
        history_kb = InlineKeyboardMarkup(row_width=5)
        back_btn = InlineKeyboardButton(
            text='back',
            callback_data='back'
        )
        for i in range(len(dishes)):
            dish_btn = InlineKeyboardButton(
                text=str(i),
                callback_data=str(f'dish_{dishes[i].id}')
            )
            history_kb.insert(dish_btn)

        history_kb.add(back_btn)
        return history_kb


class HideDishKeyboard:
    """Keyboard to hide dishes info msg's for history state."""

    hide_kb = InlineKeyboardMarkup()
    hide_btn = InlineKeyboardButton(
        text='hide',
        callback_data='hide'
    )
    hide_kb.add(hide_btn)


start_kb = StartKeyboard.start_kb
choose_kb = ChooseDishKeyboard.choose_kb
more_kb = MoreInfoKeyboard.more_kb
hide_dish_kb = HideDishKeyboard.hide_kb
