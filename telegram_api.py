import os

import aiogram
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
import logging

from aiogram.dispatcher.storage import FSMContextProxy

from db.users import UserModel
from db.dishes import DishModel
from markup import FindDishState, start_kb, choose_kb, more_kb

from controller import DishBotController, DishApiRepr

from db_manager import DBManager

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
storage = MemoryStorage()
bot = Bot(TELEGRAM_TOKEN)
dp = Dispatcher(bot, storage=storage)

logging.basicConfig(level=logging.DEBUG)

controller = DishBotController()
db_manager = DBManager()


async def on_startup(_):
    print('RUNNING')


@dp.message_handler(Text(equals='Find dish'))
async def find_dish_event(message: types.Message, state: FSMContext):
    await message.answer("Enter your ingredients split by ',' ")
    await FindDishState.enter_ingredients.set()

    async with state.proxy() as data:
        data['chat_id'] = message.from_user.id
        data['cur_dish_id'] = 0

    await message.delete()


@dp.message_handler(Text(equals='History'))
async def find_dish_event(message: types.Message):
    db_manager.test_print_dish()
    await message.delete()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(
        chat_id=message.from_user.id,
        text='HI HI HI HI',
        reply_markup=start_kb,
    )
    user = UserModel(tg_id=message.from_user.id)
    db_manager.add_user(user)


test_input = 'apples,flour,sugar'


async def show_dish_info(title, image_url, chat_id):
    await bot.send_photo(
        chat_id=chat_id,
        reply_markup=choose_kb,
        photo=image_url,
        caption=title,
    )


@dp.message_handler(state=FindDishState.enter_ingredients)
async def find_dish(message: types.Message, state: FSMContext):
    ingredients = message.text
    controller.run(test_input)
    dishes = controller.get_dishes()
    await message.answer(ingredients)
    async with state.proxy() as data:
        data['dishes'] = dishes
        dish = _get_cur_dish(data)
        try:
            await show_dish_info(
                chat_id=data['chat_id'],
                image_url=dish.image_url,
                title=dish.title,
            )
        except IndexError:  # dont work. need async version???
            print('no dishes')


def _add_dish_to_db(dish: DishApiRepr):
    dish_model = DishModel(
        id=dish.id,
        title=dish.title,
        image_url=dish.image_url,
        instruction=dish.instruction
    )
    db_manager.add_dish(dish_model)


@dp.callback_query_handler(state=FindDishState.more_info)
async def more_info_state(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        dish: DishApiRepr = _get_cur_dish(data)

    if callback.data == 'back':
        await callback.message.delete()
        async with state.proxy() as data:
            await show_dish_info(
                chat_id=data['chat_id'],
                image_url=dish.image_url,
                title=dish.title
            )

        await FindDishState.enter_ingredients.set()
        await callback.answer('back')

    elif callback.data == 'save':
        _add_dish_to_db(dish)
        await callback.answer('SAVED!')


async def to_start(callback):
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


def _get_cur_dish(data: FSMContextProxy):
    return data['dishes'][data['cur_dish_id']]


def _next_dish(data: FSMContextProxy):
    cur_dish_id = data['cur_dish_id']
    data['cur_dish_id'] = min(cur_dish_id + 1, len(data['dishes']) - 1)


def _prev_dish(data: FSMContextProxy):
    cur_dish_id = data['cur_dish_id']
    data['cur_dish_id'] = max(cur_dish_id - 1, 0)


@dp.callback_query_handler(state=FindDishState.enter_ingredients)
async def dish_list_keyboard_handler(
        callback: types.CallbackQuery,
        state: FSMContext):
    if callback.data == 'prev':
        async with state.proxy() as data:
            _prev_dish(data)
            dish = _get_cur_dish(data)
            await update_dish_message(callback, dish)
            await callback.answer('prev')

    elif callback.data == 'next':
        async with state.proxy() as data:
            _next_dish(data)
            dish = _get_cur_dish(data)
            await update_dish_message(callback, dish)
            await callback.answer('next')

    elif callback.data == 'more':
        await callback.message.delete()
        async with state.proxy() as data:
            dish = _get_cur_dish(data)
            await callback.message.answer(
                text=dish.instruction,
                reply_markup=more_kb,
            )
        await FindDishState.more_info.set()
        await callback.answer()

    elif callback.data == 'stop':
        await to_start(callback)
        await state.finish()


def run():
    executor.start_polling(dp, on_startup=on_startup)
