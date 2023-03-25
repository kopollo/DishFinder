from . import db_session
from .dishes import DishModel
from .users import UserModel
from .users_to_dishes import UsersToDishesModel


class DBManager:

    def add_dish(self, dish: DishModel):
        db_sess = db_session.create_session()
        db_sess.merge(dish)
        db_sess.commit()

    # def get_dish(self, dish_id: int):
    # db_sess = db_session.create_session()
    # db_sess.query(User).filter(User.email == form.email.data).first():

    def add_user(self, user: UserModel):
        db_sess = db_session.create_session()
        db_sess.merge(user)
        db_sess.commit()

    def test_print_dish(self):
        db_sess = db_session.create_session()
        dish = db_sess.query(DishModel).all()
        for i in dish:
            print(i)

    def add_user_to_dish_association(self,
                                     user_id: UserModel,
                                     dish_id: DishModel):
        db_sess = db_session.create_session()
        association = UsersToDishesModel(
            user_id=user_id,
            dish_id=dish_id,
        )
        db_sess.merge(association)
        db_sess.commit()

    def get_all_user_dishes(self, user: UserModel) -> list[DishModel]:
        db_sess = db_session.create_session()
        dishes = db_sess.query(UsersToDishesModel).filter(
            UsersToDishesModel.user_id == user.tg_id
        ).all()
        dishes = [record.dish for record in dishes]
        # for row in a:
        #     row: DishModel
        #     print(row.title)
        return dishes
