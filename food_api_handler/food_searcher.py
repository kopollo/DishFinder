"""Contain DishBotController, DishApiRepr."""
from typing import Optional

from .requests_wrapper import SearchByIngredientsRequest, \
    GetRecipeInstructionsRequest
from dataclasses import dataclass


@dataclass()
class DishApiRepr:
    """Representation of dish api object."""

    title: str
    id: int
    image_url: str
    instruction: str


class DishBotController:
    """Handler food api requests."""

    def __init__(self):
        """Init DishBotController."""
        self.ingredients = None
        self.dishes = []

        self.answer = []  # RENAME

    def run(self, user_input):
        """
        Make a SearchByIngredientsRequest to api and get all dishes.

        :param user_input: user input ingredients
        :return: None
        """
        self.ingredients = user_input
        self.dishes = \
            SearchByIngredientsRequest(self.ingredients).get_all_dishes()

    def generate_instruction(self, dish_id) -> Optional[str]:
        """
        Make a GetRecipeInstructionsRequest and format it like a string.

        :param dish_id: api id for dish.
        :return: None or str
        """
        instruction = GetRecipeInstructionsRequest(
            dish_id,
        ).get_instruction()
        if instruction is not None:  # CHECK THAT RECIPE is existed
            return self._format_instruction(instruction)
        return None

    def _format_instruction(self, instruction: list):
        formatted_instruction = ""
        for idx, step in enumerate(instruction):
            line = f'{idx + 1}) {step}\n\n'
            formatted_instruction += line
        return formatted_instruction

    def _generate_dish_list_for_answer(self):
        """Generate list of dishes for output."""
        for dish in self.dishes:
            title, dish_id, image_url = dish
            instruction = self.generate_instruction(dish_id)
            if instruction is not None:
                dish = DishApiRepr(
                    title=title,
                    id=dish_id,
                    image_url=image_url,
                    instruction=instruction
                )
                self.answer.append(dish)

    def get_dishes(self) -> list[DishApiRepr]:
        """Return list[DishApiRepr] by user input."""
        self._generate_dish_list_for_answer()
        return self.answer
