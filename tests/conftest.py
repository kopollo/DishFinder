"""Contain fixtures, that initialize mock sqlalchemy session / test models"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from db import db_session, UserModel
from db.db_session import SqlAlchemyBase
from db.dishes import DishModel
import db.crud_wrappers as DBManager

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
def mock_db_manager(monkeypatch, correct_dish, session):
    """Create db_manager with replaced mock session creator."""

    def mockreturn():
        return session

    db_manager = DBManager
    monkeypatch.setattr(
        db_session, "create_session", mockreturn)
    yield db_manager


@pytest.fixture
def correct_dish():
    dish = DishModel(
        id=1,
        title='x',
        instruction="x",
    )
    yield dish


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
