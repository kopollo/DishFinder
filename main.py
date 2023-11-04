"""Entrance point of program."""
from pydantic import BaseModel

from db import db_session
from db.repositories import DishRepository, UserRepository
#
# from services.dish_service import DishService
# from services.setup import dish_service, user_service
# from food_api_handler import manager as dish_searcher

if __name__ == "__main__":
    db_session.global_init('db/dish_finder.db')
    from bot import handlers
    s = db_session.create_session()
    dish_repository = DishRepository(s)
    user_repository = UserRepository(s)
    handlers.run()
