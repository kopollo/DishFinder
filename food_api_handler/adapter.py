"""Contain dish api adapter to core."""
from dataclasses import asdict

from bot_handler.bot_context import DishInBotRepr
from bot_handler.services.dish_search_port import BaseDishSearcher
from food_api_handler.food_searcher import FoodApiManager
from food_api_handler.requests_wrapper import DishApiRepr


class FoodApiAdapter(BaseDishSearcher):
    """Adapter for dish search port from core package."""

    def _from_api_to_tg_dish(self, dish: DishApiRepr):
        """Translate DishApiRepr to DishInBotRepr."""
        dish_repr = DishInBotRepr(**asdict(dish))
        return dish_repr

    def get_dishes(self, ingredients: str) -> list[DishInBotRepr]:
        """Return list of dishes in DishInBotRepr."""
        dishes = FoodApiManager(ingredients).get_dishes()
        dishes = list(map(self._from_api_to_tg_dish, dishes))
        return dishes
