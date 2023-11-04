"""Contain fixtures, that initialize mock sqlalchemy session / test models"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from db import db_session, UserModel
from db.db_session import SqlAlchemyBase
from db.dishes import DishModel
from db.repositories import DishRepository, UserRepository
from services.dto_models import DishDTO

test_db_url = f'sqlite:///tests/test_dish_finder.db?check_same_thread=False'


@pytest.fixture(scope="function")
def engine():
    engine = create_engine(
        test_db_url,
        echo=False
    )
    SqlAlchemyBase.metadata.drop_all(engine)
    SqlAlchemyBase.metadata.create_all(engine)
    try:
        yield engine
    finally:
        SqlAlchemyBase.metadata.drop_all(engine, checkfirst=True)


@pytest.fixture
def session(engine):
    session = Session(engine)
    yield session
    session.close()


@pytest.fixture
def dish_repository(monkeypatch, correct_dish, session):
    """Create db_manager with replaced mock session creator."""

    def mockreturn():
        return session

    dish_repository = DishRepository(db_session)
    monkeypatch.setattr(
        db_session, "create_session", mockreturn)
    yield dish_repository


# @pytest.fixture
# def user_repository(monkeypatch, session):
#     """Create db_manager with replaced mock session creator."""
#
#     def mockreturn():
#         return session
#
#     user_repository = UserRepository(db_session)
#     monkeypatch.setattr(
#         db_session, "create_session", mockreturn)
#     yield user_repository


@pytest.fixture
def correct_dish():
    d = {
        "id": 1,
        "title": 'xx',
        "instruction": "xx",
    }
    # dish =
    yield DishDTO.model_validate(d)


@pytest.fixture
def incorrect_dish():
    dish = DishModel(
        id='x',
        title=1123,
    )
    yield dish


@pytest.fixture
def correct_user():
    user = UserModel(
        tg_id=1
    )
    yield user


@pytest.fixture
def incorrect_user():
    user = UserModel(
        tg_id='x',
    )
    yield user
