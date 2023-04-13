"""Wrappers for food api requests."""
import os
from typing import Optional

import requests

from dataclasses import dataclass

FOOD_API_TOKEN = os.environ.get('FOOD_API_TOKEN')


@dataclass()
class DishApiRepr:
    """Representation of dish api object."""

    title: str
    id: int
    image_url: str
    ingredients: str
    instruction: str = ""


class SearchByIngredientsRequest:
    """Wrapper for findByIngredients request."""

    API_URL = 'https://api.spoonacular.com/recipes/findByIngredients'

    def __init__(self, ingredients):
        """Init obj to search full recipe."""
        self.ingredients = ingredients
        self.dish_number = 1
        self.raw_json = self._get_raw_json()

    def _get_raw_json(self):
        params = {
            'ingredients': self.ingredients,
            'apiKey': FOOD_API_TOKEN,
            'number': self.dish_number
        }
        response = get_request(
            server=self.API_URL,
            params=params
        )
        return response.json()

    def init_dishes(self) -> list[DishApiRepr]:
        """
        Extract from the json require dish info.

        :return: tuple(title, id, image_url)
        """
        dishes: list[DishApiRepr] = []
        for i in range(len(self.raw_json)):
            title = self.raw_json[i]['title']
            dish_id = self.raw_json[i]['id']
            image_url = self.raw_json[i]['image']
            ingredients = self._get_dish_ingredients(self.raw_json[i])
            dishes.append(DishApiRepr(
                title=title,
                id=dish_id,
                image_url=image_url,
                ingredients=ingredients,
            ))
        return dishes

    def _get_dish_ingredients(self, row) -> str:
        ingredients = []
        for ingredient in (row["usedIngredients"]):
            ingredients.append(ingredient['original'])

        for ingredient in (row["missedIngredients"]):
            ingredients.append(ingredient['original'])

        return self._format_ingredients(ingredients)

    def _format_ingredients(self, ingredients: list[str]) -> str:
        formatted_ingredients = ""
        for idx, eng in enumerate(ingredients):
            line = f'{idx + 1}) {eng}\n\n'
            formatted_ingredients += line
        return formatted_ingredients


class GetRecipeInstructionsRequest:
    """Wrapper for get analyzedInstructions request."""

    def __init__(self, dish_id):
        """
        Init api url by dish_id.

        :param dish_id:
        """
        self.dish_id = dish_id
        self.api_url = f'https://api.spoonacular.com/recipes/{dish_id}/analyzedInstructions'
        self.raw_json = self._get_raw_json()

    def _get_raw_json(self):
        """Make a get request."""
        params = {
            'apiKey': FOOD_API_TOKEN,
        }
        response = get_request(
            self.api_url,
            params,
        )
        return response.json()

    def get_instruction(self) -> Optional[str]:
        """
        Get full instruction for dish or None if broken or incorrect dish.

        :return: str or None
        """
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

    def _format_instruction(self, instruction: list):
        formatted_instruction = ""
        for idx, step in enumerate(instruction):
            line = f'{idx + 1}) {step}\n\n'
            formatted_instruction += line
        return formatted_instruction


def get_request(server: str, params: dict[str, str] = None):
    """
    Make GET request to server with given params.

    :param server: where we want to make a request
    :param params: with what parameters
    :return: response
    """
    try:
        response = requests.get(server, params)
        if not response:
            print('Server is sad with status code', response.status_code)
            print(response.reason)
            return response
        return response
    except requests.RequestException as exc:
        print('Oh ship :(')
        print(exc)
