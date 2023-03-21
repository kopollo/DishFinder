from db import db_session
from db.dishes import DishModel
from db.users import UserModel
from db.users_to_dishes import UsersToDishesModel


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

    def add_user_to_dish_association(self, user: UserModel, dish: DishModel):
        db_sess = db_session.create_session()
        association = UsersToDishesModel(
            user=user,
            dish=dish,
        )
        db_sess.merge(association)
        db_sess.commit()

    def get_all_user_dishes(self):
        pass


db_manager = DBManager()
