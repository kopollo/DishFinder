"""Contain initialization of bot, db, fsm storage, logger."""
import os
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from lang_translator.translator import LangTranslator
from services.dish_service import DishService
from services.setup import dish_service, user_service
from food_api_handler import manager as dish_searcher
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
bot = Bot(TELEGRAM_TOKEN)
fsm_storage = MemoryStorage()
dp = Dispatcher(bot, storage=fsm_storage)
logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.INFO)
# db_manager: BaseStorage = DBAdapter()
# dish_searcher: BaseDishSearcher = FoodApiAdapter()
lang_translator: LangTranslator = LangTranslator()

# db_manager = None
# from db import db_session
