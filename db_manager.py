from db import db_session
from db.dishes import DishModel
from db.users import UserModel


class DBManager:

    def add_dish(self, dish: DishModel):
        db_sess = db_session.create_session()
        db_sess.merge(dish)
        db_sess.commit()

    def add_user(self, user: UserModel):
        db_sess = db_session.create_session()
        db_sess.merge(user)
        db_sess.commit()

    def test_print_dish(self):
        db_sess = db_session.create_session()
        dish = db_sess.query(DishModel).all()
        for i in dish:
            print(i)
