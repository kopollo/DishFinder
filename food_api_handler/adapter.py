from dataclasses import asdict

from bot_handler.bot_context import DishInBotRepr
from food_api_handler.food_searcher import FoodApiManager
from food_api_handler.requests_wrapper import DishApiRepr


def _from_api_to_tg_dish(dish: DishApiRepr):
    """Translate DishApiRepr to DishInBotRepr."""
    dish_repr = DishInBotRepr(**asdict(dish))
    return dish_repr


def get_dishes(ingredients: str) -> list[DishInBotRepr]:
    dishes = FoodApiManager(ingredients).get_dishes()
    dishes = [_from_api_to_tg_dish(dish) for dish in dishes]
    return dishes
