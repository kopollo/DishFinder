import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, Command

from markup import FindDishState, start_kb, choose_kb, more_kb

from controller import DishBotController

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
storage = MemoryStorage()
bot = Bot(TELEGRAM_TOKEN)
dp = Dispatcher(bot, storage=storage)


async def on_startup(_):
    print('RUNNING')


@dp.message_handler(Text(equals='Find dish'))
async def start(message: types.Message):
    await message.answer("Enter your ingredients split by ',' ")

    await FindDishState.ingredients.set()

    await message.delete()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(
        chat_id=message.from_user.id,
        text='HI HI HI HI',
        reply_markup=start_kb,
    )


@dp.message_handler(state=FindDishState.ingredients)
async def process_ingredients(message: types.Message, state: FSMContext):
    ingredients = message.text
    await message.answer(ingredients)
    data = DishBotController()
    data.run(1)
    image_url = data.answer[0]['image_url']
    await bot.send_photo(
        chat_id=message.from_user.id,
        reply_markup=choose_kb,
        photo=image_url,
    )
    await state.finish()


async def print_full_recipe(callback):
    await bot.send_message(
        chat_id=callback.from_user.id,
        text='SOLD',
        reply_markup=more_kb,
    )
    await callback.answer()


async def to_start(callback):
    await callback.message.answer(text='BACK TO MAIN',
                                  reply_markup=start_kb)
    await callback.message.delete()
    await callback.answer()


@dp.callback_query_handler()
async def callback_handler(callback: types.CallbackQuery):
    if callback.data == 'back':
        await callback.answer('back')

    elif callback.data == 'next':
        await callback.answer('next')

    elif callback.data == 'more':
        await print_full_recipe(callback)

    elif callback.data == 'stop':
        await to_start(callback)


def run():
    executor.start_polling(dp, on_startup=on_startup)
