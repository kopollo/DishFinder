"""Entrance point of program."""
from db import db_session
from bot_handler import dp_handlers
if __name__ == "__main__":
    db_session.global_init('db/dish_finder.db')
    dp_handlers.run()

