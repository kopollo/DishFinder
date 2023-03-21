from aiogram.dispatcher.storage import FSMContextProxy


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