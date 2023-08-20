"""Wrappers for food api requests."""
import os
from typing import Optional

from pydantic import BaseModel, Field

from web_utils import get_request

FOOD_API_TOKEN = os.environ.get('FOOD_API_TOKEN')


class DishApiRepr(BaseModel):
    """Representation of dish api object."""

    title: str
    id: int
    image_url: str = Field(alias='image')
    ingredients: str = ""
    instruction: str = ""


class SearchByIngredientsRequest:
    """Wrapper for findByIngredients request."""

    API_URL = 'https://api.spoonacular.com/recipes/findByIngredients'
    DISH_NUMBER = 5

    def __init__(self, ingredients: str):
        """Init obj to search full recipe."""
        self.ingredients = ingredients
        self.raw_json = self._get_raw_json()

    def _get_raw_json(self):
        params = {
            'ingredients': self.ingredients,
            'apiKey': FOOD_API_TOKEN,
            'number': self.DISH_NUMBER
        }
        response = get_request(
            server=self.API_URL,
            params=params
        )
        # print(response.url)
        return response.json()

    def init_dishes(self) -> list[DishApiRepr]:
        """
        Extract from the json require dish info.

        :return: tuple(title, id, image_url)
        """
        dishes: list[DishApiRepr] = []
        for i in range(len(self.raw_json)):
            dish = DishApiRepr.model_validate(self.raw_json[i])
            ingredients = self._get_dish_ingredients(self.raw_json[i])
            dish.ingredients = ingredients
            dishes.append(dish)
        return dishes

    def _get_dish_ingredients(self, row: dict) -> str:
        """
        Extract ingredients from json.

        :param row: dish json record
        :return: formatted str with ingredients
        """
        ingredients = []
        for ingredient in (row["usedIngredients"]):
            ingredients.append(ingredient['original'])

        for ingredient in (row["missedIngredients"]):
            ingredients.append(ingredient['original'])

        return self._format_ingredients(ingredients)

    def _format_ingredients(self, ingredients: list[str]) -> str:
        """
        Format list of ingredients to str with numeration.

        :param ingredients: list of ingredients
        :return: str
        """
        formatted_ingredients = ""
        for idx, eng in enumerate(ingredients):
            line = f'{idx + 1}) {eng}\n'
            formatted_ingredients += line
        return formatted_ingredients


class GetRecipeInstructionsRequest:
    """Wrapper for get analyzedInstructions request."""

    def __init__(self, dish_id):
        """Init api url by dish_id."""
        self.dish_id = dish_id
        self.api_url = f'https://api.spoonacular.com/recipes/{dish_id}/analyzedInstructions'  # noqa
        self.raw_json = self._get_raw_json()

    def _get_raw_json(self):
        """Make a get request."""
        params = {
            'apiKey': FOOD_API_TOKEN,
        }
        try:
            response = get_request(
                self.api_url,
                params,
            )
            return response.json()
        except Exception:
            # refactor - looks terrible
            return {}

    def get_instruction(self) -> Optional[str]:
        """Get full instruction for dish or None if broken or incorrect dish."""
        # refactor None to raise NonDishException
        try:
            steps = self.raw_json[0]['steps']
        except IndexError:
            return None
        if len(steps) <= 1:
            return None

        instruction = []
        for i in range(len(steps)):
            instruction.append(steps[i]["step"])
        return self._format_instruction(instruction)

    def _format_instruction(self, instruction: list) -> str:
        """
        Format list of instruction actions to str.

        :param instruction: list of instruction
        :return: str
        """
        formatted_instruction = ""
        for idx, step in enumerate(instruction):
            line = f'{idx + 1}) {step}\n\n'
            formatted_instruction += line
        return formatted_instruction
