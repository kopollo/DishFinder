from aiogram.dispatcher.storage import FSMContextProxy

from bot_handler.setup import db_manager
from controller import DishApiRepr
from db.dishes import DishModel
from db.users import UserModel


def get_cur_dish(data: FSMContextProxy):
    return data['dishes'][data['cur_dish_id']]


def get_cur_user(data: FSMContextProxy):
    return data['user']


def next_dish(data: FSMContextProxy):
    cur_dish_id = data['cur_dish_id']
    data['cur_dish_id'] = min(cur_dish_id + 1, len(data['dishes']) - 1)


def prev_dish(data: FSMContextProxy):
    cur_dish_id = data['cur_dish_id']
    data['cur_dish_id'] = max(cur_dish_id - 1, 0)


def save_dish_event(dish_model: DishModel, user_model: UserModel):
    db_manager.add_dish(dish_model)
    db_manager.add_user_to_dish_association(
        dish_id=dish_model.id,
        user_id=user_model.tg_id,
    )


def from_dish_api_repr(dish: DishApiRepr):
    dish_model = DishModel(
        id=dish.id,
        title=dish.title,
        image_url=dish.image_url,
        instruction=dish.instruction
    )
    return dish_model

