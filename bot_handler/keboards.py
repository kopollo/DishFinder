"""Contain keyboards."""
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, \
    KeyboardButton, InlineKeyboardButton
from .bot_context import DishInBotRepr


class StartKeyboard:
    """Keyboard for start state."""

    start_kb = ReplyKeyboardMarkup(resize_keyboard=True,
                                   one_time_keyboard=True)
    find_dish_btn = KeyboardButton('/find_dish', )
    history_btn = KeyboardButton('/history')
    settings_btn = KeyboardButton('/settings')
    start_kb.add(find_dish_btn, history_btn, settings_btn)

    def __new__(cls):
        """Return keyboard if calling class."""
        return cls.start_kb


back_btn = InlineKeyboardButton(
    text='back',
    callback_data='back'
)


class ChooseDishKeyboard:
    """keyboard for dishes pagination for show_dishes state."""

    choose_kb = InlineKeyboardMarkup(row_width=3)
    prev_btn = InlineKeyboardButton(
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
    choose_kb.add(prev_btn, more_btn, next_btn, stop_btn)

    def __new__(cls):
        """Return keyboard if calling class."""
        return cls.choose_kb


class ShowInstructionInSearchKeyboard:
    """Keyboard for show_instruction state."""

    kb = InlineKeyboardMarkup()
    save_btn = InlineKeyboardButton(
        text='save recipe',
        callback_data='save',
    )
    kb.add(back_btn, save_btn)

    def __new__(cls):
        """Return keyboard if calling class."""
        return cls.kb


class HistoryKeyboard:
    """Autogenerated Keyboard for user history state."""

    @staticmethod
    def _generate_kb(dishes: list[DishInBotRepr]) -> InlineKeyboardMarkup:
        """
        Generate keyboard of DishInBotRepr obj with callback view as dish_{id}.

        :param dishes: list[DishInBotRepr]
        :return: InlineKeyboardMarkup
        """
        history_kb = InlineKeyboardMarkup(row_width=5)

        for i in range(len(dishes)):
            dish_btn = InlineKeyboardButton(
                text=str(i),
                callback_data=str(f'dish_{dishes[i].id}')
            )
            history_kb.insert(dish_btn)

        history_kb.add(back_btn)
        return history_kb

    def __new__(cls, dishes: list[DishInBotRepr]) -> InlineKeyboardMarkup:
        """Return keyboard if calling class."""
        return cls._generate_kb(dishes)


class HistoryDishInfoKeyboard:
    """Keyboard for show_history_dish state."""

    kb = InlineKeyboardMarkup()
    save_btn = InlineKeyboardButton(
        text='show instruction',
        callback_data='show_instruction',
    )
    kb.add(back_btn, save_btn)

    def __new__(cls):
        """Return keyboard if calling class."""
        return cls.kb


class HistoryDishInstructionKeyboard:
    """Keyboard for show dish instruction state."""

    kb = InlineKeyboardMarkup()
    kb.add(back_btn)

    def __new__(cls):
        """Return keyboard if calling class."""
        return cls.kb


class SettingsKeyboard:
    """Keyboard for settings state."""

    kb = InlineKeyboardMarkup(row_width=2)

    eng = InlineKeyboardButton(
        text='eng',
        callback_data='eng',
    )
    ru = InlineKeyboardButton(
        text='ru',
        callback_data='ru',
    )
    kb.add(eng, ru, back_btn)

    def __new__(cls):
        """Return keyboard if calling class."""
        return cls.kb
