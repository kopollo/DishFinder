import pytest
from sqlalchemy.exc import IntegrityError


def test_add_then_get_correct_dish(mock_db_manager, correct_dish):
    mock_db_manager.add_dish(correct_dish)
    ans = mock_db_manager.get_dish(1)
    assert ans.title == 'x' and ans.instruction == 'x'


@pytest.mark.xfail(raises=IntegrityError)
def test_add_incorrect_dish(mock_db_manager, incorrect_dish):
    mock_db_manager.add_dish(incorrect_dish)


def test_add_then_get_correct_user(mock_db_manager, correct_user):
    mock_db_manager.add_user(correct_user)
    ans = mock_db_manager.get_user(1)
    assert ans.tg_id == 1


@pytest.mark.xfail(raises=IntegrityError)
def test_add_incorrect_user(mock_db_manager, incorrect_user):
    mock_db_manager.add_user(incorrect_user)


def test_get_all_user_dishes(mock_db_manager, correct_user):
    mock_db_manager.add_user(correct_user)
    ans = mock_db_manager.get_all_user_dishes(1)
    assert ans == []


def test_save_dish_event_then_get_it(mock_db_manager, correct_dish,
                                     correct_user):
    mock_db_manager.save_dish_event(correct_dish, correct_user)
    ans = mock_db_manager.get_all_user_dishes(1)[0]
    assert ans.title == 'x'


@pytest.mark.xfail(raises=IndexError)
def test_save_dish_event_with_wrong_idx(mock_db_manager, correct_dish,
                                        correct_user):
    mock_db_manager.save_dish_event(correct_dish, correct_user)
    ans = mock_db_manager.get_all_user_dishes(1)[23]
