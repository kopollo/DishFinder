import os

import requests

FOOD_API_TOKEN = os.environ.get('FOOD_API_TOKEN')


def get_request(server: str, params: dict[str, str] = None):
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
    API_URL = 'https://api.spoonacular.com/recipes/findByIngredients'

    def __init__(self, ingredients):
        self.ingredients = ingredients
        self.dish_number = 5
        self.row_json = self._get_row_json()

    def _get_row_json(self):
        params = {
            'ingredients': self.ingredients,
            'apiKey': FOOD_API_TOKEN,
            'number': self.dish_number  # CHECK THAT WE HAVE EXACTLY NUMBER
        }
        response = get_request(
            server=self.API_URL,
            params=params
        )
        return response.json()

    def get_all_dishes(self):
        dishes = []
        for i in range(self.dish_number):
            title = self.row_json[i]['title']
            dish_id = self.row_json[i]['id']
            image_url = self.row_json[i]['image']
            dishes.append((title, dish_id, image_url))

        return dishes

    def get_dish_ingredients(self):
        # besides instructions, we are also need a list of ingred
        pass


class GetRecipeInstructionsRequest:

    def __init__(self, dish_id):
        self.dish_id = dish_id
        self.api_url = f'https://api.spoonacular.com/recipes/{dish_id}/analyzedInstructions'
        self.row_json = self._get_row_json()

    def _get_row_json(self):
        params = {
            'apiKey': FOOD_API_TOKEN,
        }
        response = get_request(
            self.api_url,
            params,
        )
        return response.json()

    def get_instruction(self):
        try:
            steps = self.row_json[0]['steps']
        except IndexError:
            return None
        if len(steps) <= 1:
            return None

        instruction = []
        for i in range(len(steps)):
            instruction.append(steps[i]["step"])
        return instruction
