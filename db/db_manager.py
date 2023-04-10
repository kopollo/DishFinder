from sqlalchemy import desc

from . import db_session
from .dishes import DishModel
from .users import UserModel
from .users_to_dishes import UsersToDishesModel


class DBManager:

    def add_dish(self, dish: DishModel):
        db_sess = db_session.create_session()
        db_sess.merge(dish)
        db_sess.commit()

    def get_dish(self, dish_id: int) -> DishModel:
        db_sess = db_session.create_session()
        dish = db_sess.query(DishModel).filter(DishModel.id == dish_id).first()
        return dish

    def add_user(self, user: UserModel):
        db_sess = db_session.create_session()
        db_sess.merge(user)
        db_sess.commit()

    def get_user(self, user_id: int) -> UserModel:
        db_sess = db_session.create_session()
        user = db_sess.query(UserModel).filter(
            UserModel.tg_id == user_id).first()
        return user

    def is_user_exist(self, user_id: int) -> bool:
        db_sess = db_session.create_session()
        exists = db_sess.query(UserModel).filter(
            UserModel.tg_id == user_id).first() is not None
        return exists

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

    def get_all_user_dishes(self, user_id: int) -> list[DishModel]:
        db_sess = db_session.create_session()
        dishes = (
            db_sess.query(UsersToDishesModel)
            .join(DishModel)
            .filter(UsersToDishesModel.user_id == user_id)
            .order_by(desc(UsersToDishesModel.id))
        )
        dishes = [record.dish for record in dishes]
        return dishes

    def save_dish_event(self, dish_model: DishModel, user_model: UserModel):
        self.add_dish(dish_model)
        self.add_user_to_dish_association(
            dish_id=dish_model.id,
            user_id=user_model.tg_id,
        )

