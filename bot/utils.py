"""Contain utils for bot handlers."""
from typing import Union

from aiogram.dispatcher.storage import FSMContextProxy, FSMContext
from aiogram import types

from dto_models import UserDTO, DishDTO
from services import dish_service
from .keboards import StartKeyboard
# from .context import DishInBotRepr, TelegramUser
from .setup import bot, dp, lang_translator, user_service
import logging


def get_cur_dish(data: FSMContextProxy) -> DishDTO:
    """
    Extract dish from context manager.

    :param data: context manager storage
    :return: DishInBotRepr
    """
    return data['dishes'][data['cur_dish_id']]


def get_cur_user(data: FSMContextProxy) -> UserDTO:
    """
    Extract user from context manager.

    :param data: context manager storage
    :return: TelegramUser
    """
    return data['user']


def next_dish(data: FSMContextProxy):
    """
    Increase id in current user dishes list and bound it.

    :param data: context manager storage
    :return: None
    """
    cur_dish_id = data['cur_dish_id']
    data['cur_dish_id'] = min(cur_dish_id + 1, len(data['dishes']) - 1)


def prev_dish(data: FSMContextProxy):
    """
    Decrease id in current user dishes list and bound it.

    :param data: context manager storage
    :return: None
    """
    cur_dish_id = data['cur_dish_id']
    data['cur_dish_id'] = max(cur_dish_id - 1, 0)


async def to_start(update: Union[types.Message, types.CallbackQuery],
                   text: str) -> None:
    """
    Reset state and send message.

    :param update: aiogram object with input data
    :param text: text
    :return: None
    """
    state = get_cur_state(get_chat_id(update))
    await state.reset_state(with_data=False)
    await send_text_msg(
        update=update,
        text=text,
        keyboard=StartKeyboard(),
    )


async def init_fsm_proxy(state: FSMContext, to_store: dict):
    """
    Initialize user session dict with data.

    :param state: position in the final state machine
    :param to_store: dict with info to store
    :return:
    """
    async with state.proxy() as data:
        for key, value in to_store.items():
            data[key] = value


# def get_user_dishes(user_id: int) -> list[DishDTO]:
#     """Get last 10 dishes from db_manager."""
#     dishes = user_service.get_user_dishes(user_id)
#     #  = filter_dishes(
#     #     user_repository.get_all_user_dishes(user_id)
#     # )
#     return dishes


async def save_history_dish_in_proxy(dish: DishDTO, state: FSMContext):
    """Save chose dish from history to proxy."""
    async with state.proxy() as data:
        data['history_dish'] = dish


async def get_proxy_history_dish(state: FSMContext) -> DishDTO:
    """Get saved dish in proxy."""
    async with state.proxy() as data:
        return data['history_dish']


def get_chat_id(update: Union[types.Message, types.CallbackQuery]) -> int:
    """Extract chat id by Update object."""
    return update.from_user.id


def get_cur_state(chat_id: int) -> FSMContext:
    """Get current state in FSM."""
    state = dp.current_state(chat=chat_id, user=chat_id)
    return state


async def send_text_msg(update: Union[types.Message, types.CallbackQuery],
                        text: str,
                        keyboard=None) -> None:  # forget about type
    """
    Send text simple message with or without keyboard.

    :param update: aiogram object with input data
    :param text: text
    :param keyboard: KeyboardMarkup
    :return: None
    """
    user_lang = user_service.get(get_chat_id(update)).language
    text = lang_translator.translate(text=text, to_lang=user_lang)
    await bot.send_message(
        chat_id=get_chat_id(update),
        text=text,
        reply_markup=keyboard,
    )


async def send_msg_with_dish(
        update: Union[types.Message, types.CallbackQuery],
        dish: DishDTO,
        keyboard=None) -> None:
    """
    Send message with dish info.

    :param update: aiogram object with input data
    :param dish: DishInBotRepr
    :param keyboard: KeyboardMarkup
    :return: None
    """
    user_lang = user_service.get(get_chat_id(update)).language
    text = lang_translator.translate(text=dish.preview(), to_lang=user_lang)
    # text = LangChecker(get_chat_id(update)).to_user_lang(dish.preview())
    logging.info(dish.title + " " + str(update.from_user.id))
    await bot.send_photo(
        chat_id=get_chat_id(update),
        reply_markup=keyboard,
        photo=dish.image_url,
        caption=text,
    )


def init_user_by_update(update: Union[types.Message, types.CallbackQuery]):
    """
    Init UserDTO object by update.

    :param update: aiogram object with input data
    :return: TelegramUser
    """
    return UserDTO(
        first_name=update.from_user.first_name,
        last_name=update.from_user.last_name,
        tg_id=update.from_user.id,
        language="en",
    )
