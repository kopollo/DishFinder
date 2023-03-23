from aiogram.dispatcher.storage import FSMContextProxy
import aiogram
from aiogram import types
from dataclasses import dataclass, asdict
from db import DishModel, UserModel
from .setup import bot, db_manager
from .markup import start_kb, choose_kb

from food_api_handler.controller import DishApiRepr


def get_cur_dish(data: FSMContextProxy):
    return data['dishes'][data['cur_dish_id']]


def get_cur_user(data: FSMContextProxy):
    return data['user']


def next_dish(data: FSMContextProxy):
    cur_dish_id = data['cur_dish_id']
    data['cur_dish_id'] = min(cur_dish_id + 1, len(data['dishes']) - 1)


def prev_dish(data: FSMContextProxy):
    cur_dish_id = data['cur_dish_id']
    data['cur_dish_id'] = max(cur_dish_id - 1, 0)


def save_dish_event(dish_model: DishModel, user_model: UserModel):
    db_manager.add_dish(dish_model)
    db_manager.add_user_to_dish_association(
        dish_id=dish_model.id,
        user_id=user_model.tg_id,
    )


def from_dish_api_repr(dish: DishApiRepr):
    dish_model = DishModel(**asdict(dish))
    return dish_model


async def to_start(callback: types.CallbackQuery):
    await callback.message.answer(text='BACK TO MAIN',
                                  reply_markup=start_kb)
    await callback.message.delete()
    await callback.answer()


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


async def show_cur_dish_info(data: FSMContextProxy):
    dish = get_cur_dish(data)
    await bot.send_photo(
        chat_id=data['chat_id'],
        reply_markup=choose_kb,
        photo=dish.image_url,
        caption=dish.title,
    )
