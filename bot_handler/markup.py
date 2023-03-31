from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, \
    KeyboardButton, InlineKeyboardButton


class FindDishState(StatesGroup):
    enter_ingredients = State()
    show_dishes = State()
    more_info = State()
    history = State()


class StartKeyboard:
    start_kb = ReplyKeyboardMarkup(resize_keyboard=True,
                                   one_time_keyboard=True)
    find_dish_btn = KeyboardButton(
        text='Find dish',
    )
    history_btn = KeyboardButton('History')
    start_kb.add(find_dish_btn, history_btn)


class ChooseDishKeyboard:
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
    pass


class HideDishKeyboard:
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