"""Entrance point of program."""
from bot import handlers
from db import db_session

if __name__ == "__main__":
    db_session.global_init('db/dish_finder.db')
    handlers.run()
