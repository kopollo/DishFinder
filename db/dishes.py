import sqlalchemy

from .db_session import SqlAlchemyBase


class Dish(SqlAlchemyBase):
    __tablename__ = 'dishes'

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
    )
    title = sqlalchemy.Column(sqlalchemy.String)
    image_url = sqlalchemy.Column(sqlalchemy.String)
    instruction = sqlalchemy.Column(sqlalchemy.String)

    def __str__(self):
        return f'<dish> {self.title} {self.image_url}'
