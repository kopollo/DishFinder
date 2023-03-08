from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, \
    KeyboardButton, InlineKeyboardButton


class FindDishState(StatesGroup):
    ingredients = State()


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
        text='back',
        callback_data='back'
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
    choose_kb.add(back_btn, next_btn, stop_btn, more_btn)


class MoreInfoKeyboard:
    more_kb = InlineKeyboardMarkup()
    yes_btn = InlineKeyboardButton(
        text='yes',
        callback_data='yes'
    )
    no_btn = InlineKeyboardButton(
        text='no',
        callback_data='no',
    )
    more_kb.add(yes_btn, no_btn)


start_kb = StartKeyboard.start_kb
choose_kb = ChooseDishKeyboard.choose_kb
more_kb = MoreInfoKeyboard.more_kb
