import telegram_api
from db import db_session
from db.dishes import Dish
from db_manager import DBManager


if __name__ == "__main__":
    db_session.global_init('db/dish_finder.db')
    dbm = DBManager()

    title = 'apple'
    instruction = 'text tet xt t et \n te x'
    idx = "1245"
    dish = Dish(
        id=idx,
        title=title,
        image_url="/fsdfsdfs",
        instruction=instruction,
    )
    dbm.test_add_dish()
    dbm.test_print_dish()
    # telegram_api.run()
