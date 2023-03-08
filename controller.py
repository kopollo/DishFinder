from food_api import SearchByIngredientsRequest, GetRecipeInstructionsRequest

d = 'apples,flour,sugar'
req = SearchByIngredientsRequest(d)


def get_formatted_dish_info():
    # idx = req.get_dish_id()
    # print(idx)
    # print(req.get_dish_image())
    # print(req.get_dish_title())
    # print()
    full = GetRecipeInstructionsRequest(1)
    full.get_instructions()
