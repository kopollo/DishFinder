import datetime

import sqlalchemy

from .db_session import SqlAlchemyBase


class UserModel(SqlAlchemyBase):
    __tablename__ = 'users'

    tg_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
    )
    modified_date = sqlalchemy.Column(
        sqlalchemy.DateTime,
        default=datetime.datetime.now,
    )



# leader = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
#     job = sqlalchemy.Column(sqlalchemy.String, nullable=True)
#     work_size = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
#     collaborators = sqlalchemy.Column(sqlalchemy.String, nullable=True)
#     start_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
#     end_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
#     is_finished = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
#
#     user = orm.relationship('User')