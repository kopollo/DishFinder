import os

from aiogram import Bot, Dispatcher, executor, types
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')

bot = Bot(TELEGRAM_TOKEN)
dp = Dispatcher(bot)


async def on_startup(_):
    print('RUNNING')


@dp.message_handler()
async def start(message: types.Message):
    await message.answer('dds')


def run():
    executor.start_polling(dp, on_startup=on_startup)

