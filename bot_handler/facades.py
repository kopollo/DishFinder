"""Contain facade for DB and API manager."""
from dataclasses import asdict
from typing import Optional

from bot_handler.bot_context import DishInBotRepr, TelegramUser
# from db.db_manager import DBManager
# from db import DishModel, UserModel
from food_api_handler.food_searcher import FoodApiManager
from food_api_handler.requests_wrapper import DishApiRepr
from db.adapter import db_adapter as adapter


# db_manager = DBManager()


class StoragePort:
    """Facade for DB package."""

    def get_dish(self, dish_id: int) -> DishInBotRepr:
        """Return a dish in DB by id and convert it to DishInBotRepr."""
        return adapter.get_dish(dish_id)

    def save_dish(self, dish: DishInBotRepr, user: TelegramUser) -> None:
        """Save a dish to user in DB."""
        return adapter.save_dish(dish, user)

    def get_user_dishes(self, user_id: int) -> list[DishInBotRepr]:
        """Return dishes in DB by user id."""
        return adapter.get_user_dishes(user_id)

    def add_user(self, user: TelegramUser) -> None:
        """Add user to DB."""
        adapter.add_user(user)

    def get_user(self, user_id) -> Optional[TelegramUser]:
        """Return user in DB, if user exist and None otherwise."""
        return adapter.get_user(user_id)


class DishSearchFilter:
    """Facade for food_api package."""

    def __init__(self, ingredients: str):
        """
        Make a coll to Food Api Manager.

        :param ingredients: str with ingredients
        """
        dishes = FoodApiManager(ingredients).get_dishes()
        self.dishes = [self._from_api_to_tg_dish(dish) for dish in dishes]

    def get_dishes(self) -> list[DishInBotRepr]:
        """Return a list of Dish objects."""
        return self.dishes

    def _from_api_to_tg_dish(self, dish: DishApiRepr):
        """Translate DishApiRepr to DishInBotRepr."""
        dish_repr = DishInBotRepr(**asdict(dish))
        return dish_repr
