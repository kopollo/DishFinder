import sqlalchemy

from .db_session import SqlAlchemyBase


class UsersToDishesModel(SqlAlchemyBase):
    __tablename__ = 'users_to_dishes'

    user_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('users.tg_id'),
        primary_key=True,

    )
    dish_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('dishes.id'),
        primary_key=True,
    )
