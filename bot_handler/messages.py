"""Contain functions that control bot messages."""
import aiogram
from aiogram.utils.exceptions import MessageNotModified
from aiogram import types
from aiogram.dispatcher.storage import FSMContextProxy, FSMContext

from food_api_handler.food_searcher import DishApiRepr
from .markup import start_kb, choose_kb, more_kb, history_dish_info_kb, \
    HistoryKeyboard, history_dish_instruction_kb
from .setup import bot, db_manager
from .utils import get_cur_dish, format_dishes_for_message, filter_dishes, \
    get_dishes_to_history
from db import DishModel


async def send_welcome_msg(chat_id):
    """
    Send welcome msg.

    :param chat_id: chat id where to send a message
    :return: None
    """
    await bot.send_message(
        chat_id=chat_id,
        text='HI HI HI HI',
        reply_markup=start_kb,
    )


# To implement multi languages better to add param text
async def send_sorry_msg(chat_id):
    """
    Send sorry msg.

    :param chat_id: chat id where to send a message
    :return: None
    """
    await bot.send_message(
        chat_id=chat_id,
        text="I'm sorry but I haven't find anything",
        reply_markup=start_kb,
    )


async def update_dish_message(callback: types.CallbackQuery, dish: DishApiRepr):
    """
    Update dish message to implement pagination.

    :param callback: callback info from pressed btn
    :param dish: DishApiRepr object
    :return: None
    """
    caption = dish.title + '\n' + '\n' + dish.ingredients
    photo = types.InputMediaPhoto(media=dish.image_url,
                                  caption=caption)
    try:
        await bot.edit_message_media(
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            media=photo,
            reply_markup=choose_kb,
        )
    except MessageNotModified:
        print('same as before')


async def send_cur_dish_info(data: FSMContextProxy):
    """
    Send current dish from context manager.

    :param data: context manager storage
    :return:
    """
    dish = get_cur_dish(data)
    caption = dish.title + '\n' + '\n' + dish.ingredients
    await bot.send_photo(
        chat_id=data['chat_id'],
        reply_markup=choose_kb,
        photo=dish.image_url,
        caption=caption,
    )


async def send_history_dish_info(callback: types.CallbackQuery,
                                 dish: DishModel) -> None:
    caption = dish.title + '\n' + '\n' + dish.ingredients
    await callback.message.delete()
    await bot.send_photo(
        chat_id=callback.from_user.id,
        reply_markup=history_dish_info_kb,
        photo=dish.image_url,
        caption=caption,
    )


async def send_dish_instruction(callback: types.CallbackQuery,
                                dish: DishApiRepr):
    """
    Send message with dish ingredients.

    :param callback: callback info from pressed btn
    :param dish: DishApiRepr
    :return: None
    """
    await callback.message.answer(
        text=dish.instruction,
        reply_markup=more_kb,
    )


async def send_history_widget(user_id: int, state: FSMContext):
    dishes = get_dishes_to_history(user_id)

    # TODO abort_if_empty_storage except (except statement) much prettier.
    try:
        await bot.send_message(
            chat_id=user_id,
            text=format_dishes_for_message(dishes),
            reply_markup=HistoryKeyboard.generate_kb(dishes),
        )
    except aiogram.utils.exceptions.MessageTextIsEmpty:
        await send_sorry_msg(user_id)
        await state.reset_state(with_data=False)


async def upd_history_widget(user_id: int, state: FSMContext):
    dishes = get_dishes_to_history(user_id)

    # TODO abort_if_empty_storage except (except statement) much prettier.
    try:
        await bot.edit_message_text(
            chat_id=user_id,
            text=format_dishes_for_message(dishes),
            reply_markup=HistoryKeyboard.generate_kb(dishes),
        )
    except aiogram.utils.exceptions.MessageTextIsEmpty:
        await send_sorry_msg(user_id)
        await state.reset_state(with_data=False)


async def show_instruction_in_history(
        callback: types.CallbackQuery,
        dish: DishApiRepr):

    await callback.message.delete()
    await callback.message.answer(
        text=dish.instruction,
        reply_markup=history_dish_instruction_kb,
    )
