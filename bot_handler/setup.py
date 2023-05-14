"""Contain initialization of bot, db, fsm storage, logger."""
import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging

from bot_handler.facades import DBFilter

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
bot = Bot(TELEGRAM_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.ERROR)
db_filter = DBFilter()
