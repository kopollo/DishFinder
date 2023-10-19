import abc

from sqlalchemy import desc

from db import UserModel, DishModel, db_session, UsersToDishesModel
from .mappers import dish_mapper, user_mapper
from dto_models import DishDTO, UserDTO


class DishRepository:
    def __init__(self, db_sess):
        self.db_sess = db_sess

    def save(self, dish: DishDTO) -> None:
        dish: DishModel = dish_mapper.to_sqlalchemy(dish)
        self.db_sess.merge(dish)
        self.db_sess.commit()

    def get(self, dish_id: int) -> DishDTO:
        dish: DishModel = self.db_sess.query(DishModel).filter(DishModel.id == dish_id).first()
        self.db_sess.close()
        return dish_mapper.to_dto(dish)


class UserRepository:
    def __init__(self, db_sess):
        self.db_sess = db_sess

    def save(self, user: UserDTO) -> None:
        user = user_mapper.to_sqlalchemy(user)
        self.db_sess.merge(user)
        self.db_sess.commit()

    def get(self, user_id: int) -> UserDTO:
        user: UserModel = self.db_sess.query(UserModel).filter(
            UserModel.tg_id == user_id).first()
        return user_mapper.to_dto(user)

    def set_lang(self, user_id: int, lang: str):
        user: UserModel = self.db_sess.query(UserModel).filter(
            UserModel.tg_id == user_id).first()
        user.language = lang
        self.db_sess.commit()

    def get_all_user_dishes(self, user_id: int) -> list[DishDTO]:
        dishes = (
            self.db_sess.query(UsersToDishesModel)
            .join(DishModel)
            .filter(UsersToDishesModel.user_id == user_id)
            .order_by(desc(UsersToDishesModel.id))
        )
        dishes: list[DishDTO] = [
            dish_mapper.to_dto(record.dish) for record in dishes
        ]
        return dishes

    def add_user_to_dish_association(self,
                                     user_id: int,
                                     dish_id: int) -> None:
        association = UsersToDishesModel(
            user_id=user_id,
            dish_id=dish_id,
        )
        self.db_sess.merge(association)
        self.db_sess.commit()
