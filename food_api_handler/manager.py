"""Contain DishBotController."""
from services.dto_models import DishDTO
from .endpoints import SearchByIngredientsRequest, \
    GetRecipeInstructionsRequest


def _set_instruction_for_dishes(dishes: list[DishDTO]) -> None:
    """Init instructions for all dishes."""
    for i, dish in enumerate(dishes):
        instruction = get_dish_instruction(dish)
        dishes[i].instruction = instruction


def get_dish_instruction(dish: DishDTO) -> str:
    """
    Get instruction for dish by api request.

    :param dish:
    :return: str
    """
    instruction = GetRecipeInstructionsRequest(dish.id).get_instruction()
    if instruction is None:
        instruction = 'No recipe found'
    return instruction


def get_dishes(ingredients: str) -> list[DishDTO]:
    dishes = SearchByIngredientsRequest(ingredients).init_dishes()
    _set_instruction_for_dishes(dishes)
    return dishes
