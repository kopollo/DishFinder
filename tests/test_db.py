# import pytest
# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker
#
#
# @pytest.fixture(scope='session')
# def db_engine():
#     """yields a SQLAlchemy engine which is suppressed after the test session"""
#     db_file = "test_dish_finder"
#     db_url = f'sqlite:///{db_file.strip()}?check_same_thread=False'
#     engine_ = create_engine(db_url, echo=True)
#     yield engine_
#     engine_.dispose()
#
#
# @pytest.fixture(scope='session')
# def db_session_factory(db_engine):
#     """returns a SQLAlchemy scoped session factory"""
#     return scoped_session(sessionmaker(bind=db_engine))
#
#
# @pytest.fixture(scope='function')
# def db_session(db_session_factory):
#     """yields a SQLAlchemy connection which is rollbacked after the test"""
#     session_ = db_session_factory()
#
#     yield session_
#
#     session_.rollback()
#     session_.close()
#
# # def test_add_dish(self):
# #     db_sess = db_session.create_session()
# #     title = 'apple'
# #     instruction = 'text tet xt t et \n te x'
# #     idx = "1245"
# #     dish = Dish(
# #         id=idx,
# #         title=title,
# #         # image_url="/fsdfsdfs",
# #         instruction=instruction,
# #     )
# #     db_sess.merge(dish)
# #     db_sess.commit()
# #
# #
# # def test_print_dish(self):
# #     db_sess = db_session.create_session()
# #     dish = db_sess.query(Dish).all()
# #     for i in dish:
# #         print(i)
