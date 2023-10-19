"""Contain initialization of bot, db, fsm storage, logger."""
import os
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# from .services.storage_port import BaseStorage
# from .services.dish_search_port import BaseDishSearcher
import food_api_handler.manager as dish_searcher
from db import db_session
from lang_translator.translator import LangTranslator

from services import dish_service, user_service
from db.repositories import UserRepository, DishRepository
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
