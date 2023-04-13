"""Wrappers for raw json."""
import os
from typing import Optional

import requests

FOOD_API_TOKEN = os.environ.get('FOOD_API_TOKEN')


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


class SearchByIngredientsRequest:
    """Wrapper for findByIngredients request."""

    API_URL = 'https://api.spoonacular.com/recipes/findByIngredients'

    def __init__(self, ingredients):
        """Init obj to search full recipe."""
        self.ingredients = ingredients
        self.dish_number = 5
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

    def get_all_dishes(self):
        """
        Extract from the json require dish info.

        :return: tuple(title, id, image_url)
        """
        dishes = []
        for i in range(len(self.raw_json)):
            title = self.raw_json[i]['title']
            dish_id = self.raw_json[i]['id']
            image_url = self.raw_json[i]['image']
            dishes.append((title, dish_id, image_url))
        return dishes

    def _get_dish_ingredients(self):
        # besides instructions, we are also need a list of ingred
        pass


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

    def get_instruction(self) -> Optional[list[str]]:
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
        return instruction
