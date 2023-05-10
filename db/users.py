"""Contain UserModel."""
import datetime

import sqlalchemy

from .db_session import SqlAlchemyBase


class UserModel(SqlAlchemyBase):
    """SqlAlchemy db model for user."""

    __tablename__ = 'users'

    tg_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
    )
    modified_date = sqlalchemy.Column(
        sqlalchemy.DateTime,
        default=datetime.datetime.now,
    )
    first_name = sqlalchemy.Column(sqlalchemy.String)
    last_name = sqlalchemy.Column(sqlalchemy.String)
    language = sqlalchemy.Column(sqlalchemy.String, default="en")
