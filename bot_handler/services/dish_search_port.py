from ..bot_context import DishInBotRepr
import food_api_handler.adapter as adapter


def get_dishes(ingredients: str) -> list[DishInBotRepr]:
    return adapter.get_dishes(ingredients)
