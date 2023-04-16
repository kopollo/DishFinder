"""Contain functions that control bot messages."""
from aiogram.utils.exceptions import MessageNotModified
from aiogram import types
from aiogram.dispatcher.storage import FSMContextProxy

from food_api_handler.food_searcher import DishApiRepr
from .markup import start_kb, choose_kb, more_kb, hide_dish_kb
from .setup import bot
from .utils import get_cur_dish
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
        pass


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


async def send_more_dish_info(callback: types.CallbackQuery, dish: DishApiRepr):
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


async def send_dish_info_for_history(callback: types.CallbackQuery,
                                     dish: DishModel):
    """
    Send message with dish photo with title for /history cmd.

    :param callback: callback info from pressed btn
    :param dish: DishModel obj
    :return: None
    """
    await callback.message.answer_photo(
        photo=dish.image_url,
        caption=dish.title,
        reply_markup=hide_dish_kb,
    )
