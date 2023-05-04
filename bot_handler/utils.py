"""Contain utils for bot handlers."""
from aiogram.dispatcher.storage import FSMContextProxy, FSMContext
from aiogram import types
from dataclasses import asdict

from db import DishModel, UserModel
from .markup import start_kb

from food_api_handler.food_searcher import DishApiRepr
from .setup import db_manager


def get_cur_dish(data: FSMContextProxy) -> DishApiRepr:
    """
    Extract dish from context manager.

    :param data: context manager storage
    :return: DishApiRepr
    """
    return data['dishes'][data['cur_dish_id']]


def get_cur_user(data: FSMContextProxy) -> UserModel:
    """
    Extract user from context manager.

    :param data: context manager storage
    :return: UserModel
    """
    return data['user']


def next_dish(data: FSMContextProxy):
    """
    Increase id in current user dishes list and bound it.

    :param data: context manager storage
    :return: None
    """
    cur_dish_id = data['cur_dish_id']
    data['cur_dish_id'] = min(cur_dish_id + 1, len(data['dishes']) - 1)


def prev_dish(data: FSMContextProxy):
    """
    Decrease id in current user dishes list and bound it.

    :param data: context manager storage
    :return: None
    """
    cur_dish_id = data['cur_dish_id']
    data['cur_dish_id'] = max(cur_dish_id - 1, 0)


def from_dish_api_repr(dish: DishApiRepr) -> DishModel:
    """
    Transfer DishApiRepr to DishModel.

    :param dish: DishApiRepr
    :return: DishModel
    """
    dish_model = DishModel(**asdict(dish))
    return dish_model


async def to_start(callback: types.CallbackQuery):
    """
    Relocate user to start state.

    :param callback: callback info from pressed btn
    :return:
    """
    text = """welcome back"""
    await callback.message.answer(text=text,
                                  reply_markup=start_kb)
    await callback.message.delete()
    await callback.answer()


def filter_dishes(dishes: list[DishModel]) -> list[DishModel]:
    """Bound dishes to show user by 10."""
    return dishes[:10]


def format_dishes_for_message(dishes: list[DishModel]) -> str:
    """
    Format dishes for bot message to show user.

    :param dishes: list of dishes
    :return: str
    """
    ans = ''
    for i, dish in enumerate(dishes):
        ans += f'{i}) {dish.title}\n'
    return ans


async def init_fsm_proxy(state: FSMContext, to_store: dict):
    """
    Initialize user session dict with data.

    :param state: position in the final state machine
    :param to_store: dict with info to store
    :return:
    """
    async with state.proxy() as data:
        for key, value in to_store.items():
            data[key] = value


def get_dishes_to_history(user_id: int) -> list[DishModel]:
    dishes = filter_dishes(
        db_manager.get_all_user_dishes(user_id)
    )
    return dishes


async def save_history_dish_in_proxy(dish: DishModel, state: FSMContext):
    async with state.proxy() as data:
        data['history_dish'] = dish


async def extract_history_dish(state: FSMContext) -> DishModel:
    async with state.proxy() as data:
        return data['history_dish']
