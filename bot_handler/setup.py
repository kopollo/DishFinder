import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
from controller import DishBotController
from db_manager import DBManager

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
storage = MemoryStorage()
bot = Bot(TELEGRAM_TOKEN)
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.DEBUG)
controller = DishBotController()
db_manager = DBManager()
