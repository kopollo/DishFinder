import telegram_api
from db import db_session


if __name__ == "__main__":
    db_session.global_init('db/dish_finder.db')
    telegram_api.run()
