"""Contain initialization of bot, db, fsm storage, logger."""
import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
from food_api_handler.food_searcher import DishBotController
from db.db_manager import DBManager

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
bot = Bot(TELEGRAM_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.ERROR)
food_searcher = DishBotController()
db_manager = DBManager()
