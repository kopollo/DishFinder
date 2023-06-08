"""Contain initialization of bot, db, fsm storage, logger."""
import os
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from .services.storage_port import BaseStorage
from db.adapter import DBAdapter

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
bot = Bot(TELEGRAM_TOKEN)
fsm_storage = MemoryStorage()
dp = Dispatcher(bot, storage=fsm_storage)
logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.INFO)

db_manager: BaseStorage = DBAdapter()
