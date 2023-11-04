from db.repositories import DishRepository, UserRepository
from .dish_service import DishService
from db import db_session
from services.user_service import UserService

s = db_session.create_session()
dish_service = DishService(DishRepository(s))
user_service = UserService(UserRepository(s), dish_service)
