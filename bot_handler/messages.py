"""Contain functions that control bot messages."""
from typing import Union

import aiogram
from aiogram.utils.exceptions import MessageNotModified
from aiogram import types
from aiogram.dispatcher.storage import FSMContextProxy, FSMContext

from food_api_handler.food_searcher import DishApiRepr
from .markup import HistoryKeyboard, HistoryDishInstructionKeyboard, \
    StartKeyboard, HistoryDishInfoKeyboard, ChooseDishKeyboard, \
    ShowInstructionKeyboard
from .setup import bot, db_manager
from .utils import get_cur_dish, format_dishes_for_message, filter_dishes, \
    get_user_dishes, from_dish_api_repr, send_text_msg, get_chat_id, \
    get_proxy_history_dish, get_cur_state, \
    send_msg_with_dish, to_start
from db import DishModel


async def update_dish_message(callback: types.CallbackQuery, dish: DishModel):
    """
    Update dish message to implement pagination.

    :param callback: callback info from pressed btn
    :param dish: DishApiRepr object
    :return: None
    """
    photo = types.InputMediaPhoto(media=dish.image_url,
                                  caption=dish.preview())
    try:
        await bot.edit_message_media(
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            media=photo,
            reply_markup=ChooseDishKeyboard(),
        )
    except MessageNotModified:
        pass


async def send_history_dish_info(callback: types.CallbackQuery) -> None:
    """Send info about dish in history - dish title, ingredients, photo."""
    chat_id = get_chat_id(callback)
    state = get_cur_state(chat_id)
    dish = await get_proxy_history_dish(state)
    await send_msg_with_dish(
        update=callback,
        keyboard=HistoryDishInfoKeyboard(),
        dish=dish,
    )


async def send_cur_dish_info(
        update: Union[types.Message, types.CallbackQuery]) -> None:
    state = get_cur_state(get_chat_id(update))
    async with state.proxy() as data:
        dish = get_cur_dish(data)
        await send_msg_with_dish(
            update=update,
            keyboard=ChooseDishKeyboard(),
            dish=dish
        )


async def send_history_widget(
        update: Union[types.Message, types.CallbackQuery]):
    """Send widget with dishes in history."""
    dishes = get_user_dishes(get_chat_id(update))
    # TODO abort_if_empty_storage except (except statement) much prettier.
    if not len(dishes):
        state = get_cur_state(get_chat_id(update))
        await to_start(update, state)
    else:
        await send_text_msg(
            update=update,
            text=format_dishes_for_message(dishes),
            keyboard=HistoryKeyboard(dishes), )
