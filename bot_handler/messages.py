import aiogram
from aiogram import types
from aiogram.dispatcher.storage import FSMContextProxy

from bot_handler.markup import *
from bot_handler.setup import *
from bot_handler.utils import get_cur_dish


async def send_welcome_msg(char_id):
    await bot.send_message(
        chat_id=char_id,
        text='HI HI HI HI',
        reply_markup=start_kb,
    )


async def update_dish_message(callback: types.CallbackQuery, dish):
    photo = types.InputMediaPhoto(media=dish.image_url,
                                  caption=dish.title)
    try:
        await bot.edit_message_media(
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            media=photo,
            reply_markup=choose_kb,
        )
    except aiogram.utils.exceptions.MessageNotModified:
        print('same as before')
        pass


async def send_cur_dish_info(data: FSMContextProxy):
    dish = get_cur_dish(data)
    await bot.send_photo(
        chat_id=data['chat_id'],
        reply_markup=choose_kb,
        photo=dish.image_url,
        caption=dish.title,
    )


async def send_more_dish_info(callback: types.CallbackQuery, dish):
    await callback.message.answer(
        text=dish.instruction,
        reply_markup=more_kb,
    )