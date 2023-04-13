"""Entrance point of program."""
# from db import db_session
# from bot_handler import dp_handlers
from food_api_handler.food_searcher import SearchByIngredientsRequest, FoodApiManager
if __name__ == "__main__":
    eng = FoodApiManager("honey")
    print(eng.dishes[0].ingredients)
    # db_session.global_init('db/dish_finder.db')
    # dp_handlers.run()

