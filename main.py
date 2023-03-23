from db import db_session
from bot_handler import logic
# import bot_handler.logic as logic
if __name__ == "__main__":
    db_session.global_init('db/dish_finder.db')
    logic.run()

