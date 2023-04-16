"""Contain DishBotController."""

from .requests_wrapper import SearchByIngredientsRequest, \
    GetRecipeInstructionsRequest, DishApiRepr


class FoodApiManager:
    """Creator and initializer of DishApiRepr objects."""

    def __init__(self, ingredients):
        """
        Init DishApiRepr objects.

        :param ingredients: user input
        """
        self.dishes = SearchByIngredientsRequest(ingredients).init_dishes()
        self._init_instruction_for_dishes()

    def _init_instruction_for_dishes(self) -> None:
        """Init instructions for all dishes."""
        for i, dish in enumerate(self.dishes):
            self._set_instruction(dish)

    def _set_instruction(self, dish: DishApiRepr):
        """
        Set instruction for dish.

        :param dish:
        :return:
        """
        dish_id = dish.id
        instruction = GetRecipeInstructionsRequest(dish_id).get_instruction()
        if instruction is None:
            instruction = 'No recipe found'
        dish.instruction = instruction

    def get_dishes(self) -> list[DishApiRepr]:
        """Return list[DishApiRepr]."""
        return self.dishes
