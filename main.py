"""Entrance point of program."""
from pydantic import BaseModel

from db import db_session, UserModel
# from db.repositories import DishRepository, UserRepository
# #

# from food_api_handler import manager as dish_searcher

if __name__ == "__main__":
    db_session.global_init('db/dish_finder.db')
    from services.dish_service import DishService
    from services.dto_models import UserDTO
    from services.setup import dish_service, user_service
    from bot import handlers
    # s = db_session.create_session()
    # dish_repository = DishRepository(s)
    # user_repository = UserRepository(s)
    # d = {
    #     "tg_id": 234,
    #     "first_name": "ab",
    #     "last_name": 'str'
    # }
    # user = UserDTO.model_validate(d)
    # print(user)
    # user_service.save(user)
    handlers.run()
