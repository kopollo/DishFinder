import json

import responses

from food_api_handler.endpoints import SearchByIngredientsRequest, \
    GetRecipeInstructionsRequest
from services.dto_models import DishDTO

TEST_DISH_ID = 633547


def _get_test_json_for_SearchByIngredientsRequest():
    return (
        [{"id": TEST_DISH_ID,
          "title": "Baked Cinnamon Apple Slices",
          "image": "cool.jpg",
          "missedIngredients": [
              {"original": "Cinnamon"},
              {"original": "Raisins"},
          ],
          "usedIngredients": [
              {"original": "Apples"}
          ],
          }
         ]
    )


def _get_test_json_for_GetRecipeInstructionsRequest():
    return json.loads(
        """[{"name":"","steps":[{"number":1,"step":"Mix ingredients together except the raisins.","ingredients":[{"id":9299,"name":"raisins","localizedName":"raisins","image":"raisins.jpg"}],"equipment":[]},{"number":2,"step":"Place in baking dish and in oven at 350 Degrees for 30 minutes.","ingredients":[],"equipment":[{"id":404646,"name":"baking pan","localizedName":"baking pan","image":"roasting-pan.jpg"},{"id":404784,"name":"oven","localizedName":"oven","image":"oven.jpg"}],"length":{"number":30,"unit":"minutes"}},{"number":3,"step":"Add raisins the last 5 minutes of baking.","ingredients":[{"id":9299,"name":"raisins","localizedName":"raisins","image":"raisins.jpg"}],"equipment":[],"length":{"number":5,"unit":"minutes"}},{"number":4,"step":"Serve and enjoy!Use Organic Ingredients if Available","ingredients":[],"equipment":[]}]}]""")


@responses.activate
def test_init_dishes_with_correct_ingredients():
    responses.add(responses.GET,
                  'https://api.spoonacular.com/recipes/findByIngredients',
                  json=_get_test_json_for_SearchByIngredientsRequest(),
                  status=200)
    dishes = SearchByIngredientsRequest('apple').init_dishes()
    data = {
        'title': 'Baked Cinnamon Apple Slices',
        'id': 633547,
        'image': 'cool.jpg',
        'ingredients': '1) Apples\n2) Cinnamon\n3) Raisins\n',
        "instruction": ''
    }
    dishes_ans = [
        DishDTO.model_validate(data)
    ]
    assert dishes == dishes_ans


@responses.activate
def test_init_dishes_with_incorrect_ingredients():
    responses.add(responses.GET,
                  'https://api.spoonacular.com/recipes/findByIngredients',
                  json="",
                  status=200)
    dishes = SearchByIngredientsRequest('FFFF').init_dishes()
    assert dishes == []


@responses.activate
def test_init_instruction():
    url = f'https://api.spoonacular.com/recipes/{TEST_DISH_ID}/analyzedInstructions'

    responses.add(responses.GET, url,
                  json=_get_test_json_for_GetRecipeInstructionsRequest(),
                  status=200)
    ins = GetRecipeInstructionsRequest(dish_id=TEST_DISH_ID)
    ans = '1) Mix ingredients together except the raisins.\n\n2) Place in baking dish and in oven at 350 Degrees for 30 minutes.\n\n3) Add raisins the last 5 minutes of baking.\n\n4) Serve and enjoy!Use Organic Ingredients if Available\n\n'
    assert ans == ins.get_instruction()


@responses.activate
def test_init_instruction_with_wrong_id():
    wrong_id = -1
    url = f'https://api.spoonacular.com/recipes/{wrong_id}/analyzedInstructions'
    responses.add(responses.GET, url,
                  json="",
                  status=200)
    ins = GetRecipeInstructionsRequest(dish_id=wrong_id)
    assert ins.get_instruction() is None
