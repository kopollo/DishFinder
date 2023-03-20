from db import db_session
from db.dishes import Dish


class DBManager:

    def add_dish(self, dish: Dish):
        db_sess = db_session.create_session()
        db_sess.merge(dish)
        db_sess.commit()

    def test_print_dish(self):
        db_sess = db_session.create_session()
        dish = db_sess.query(Dish).all()
        for i in dish:
            print(i)
