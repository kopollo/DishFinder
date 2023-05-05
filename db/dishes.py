"""Contain DishModel."""
import sqlalchemy

from .db_session import SqlAlchemyBase


class DishModel(SqlAlchemyBase):
    """SqlAlchemy db model for dish."""

    __tablename__ = 'dishes'

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
    )
    title = sqlalchemy.Column(sqlalchemy.String)
    image_url = sqlalchemy.Column(sqlalchemy.String)
    instruction = sqlalchemy.Column(sqlalchemy.String)
    ingredients = sqlalchemy.Column(sqlalchemy.String)

    def preview(self):
        return self.title + '\n' + '\n' + self.ingredients
