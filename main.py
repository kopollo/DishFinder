from db import db_session
from bot_handler import logic
if __name__ == "__main__":
    db_session.global_init('db/dish_finder.db')
    logic.run()

