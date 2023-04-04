import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase
from db.dishes import DishModel


class UsersToDishesModel(SqlAlchemyBase):
    __tablename__ = 'users_to_dishes'

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True,
    )
    user_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('users.tg_id'),

    )
    dish_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('dishes.id'),
    )
    dish = orm.relationship(DishModel)
