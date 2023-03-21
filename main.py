from bot_handler import bot_logic
from db import db_session


if __name__ == "__main__":
    db_session.global_init('db/dish_finder.db')
    bot_logic.run()
