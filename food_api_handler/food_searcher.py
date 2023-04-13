"""Contain DishBotController."""

from .requests_wrapper import SearchByIngredientsRequest, \
    GetRecipeInstructionsRequest, DishApiRepr


class FoodApiManager:
    """Handler for food api requests."""

    def __init__(self, ingredients):
        self.ingredients = ingredients
        self.dishes = SearchByIngredientsRequest(self.ingredients).init_dishes()
        self._init_instruction_for_dishes()

    def _init_instruction_for_dishes(self) -> None:
        for i, dish in enumerate(self.dishes):
            self._set_instruction(dish)

    def _set_instruction(self, dish: DishApiRepr):
        dish_id = dish.id
        instruction = GetRecipeInstructionsRequest(dish_id).get_instruction()
        dish.instruction = instruction

    def get_dishes(self) -> list[DishApiRepr]:
        """Return list[DishApiRepr] with dishes."""
        return self.dishes
