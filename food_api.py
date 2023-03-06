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


def get_dish():
    params = {
        'ingredients': 'apples,flour,sugar',
        'apiKey': FOOD_API_TOKEN,
        'number': 2
    }
    response = get_request(
        server='https://api.spoonacular.com/recipes/findByIngredients',
        params=params
    )
    return response.json()[0]['title']
