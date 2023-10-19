"""Entrance point of program."""
from pydantic import BaseModel

from db import db_session
from db.repositories import DishRepository, UserRepository


if __name__ == "__main__":
    db_session.global_init('db/dish_finder.db')
    from bot import handlers
    # s = db_session.create_session()
    # dish_repository = DishRepository(s)
    # user_repository = UserRepository(s)
    handlers.run()
