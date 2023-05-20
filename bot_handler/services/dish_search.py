from dataclasses import asdict

from ..bot_context import DishInBotRepr, TelegramUser
from food_api_handler.food_searcher import FoodApiManager
from food_api_handler.requests_wrapper import DishApiRepr


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
