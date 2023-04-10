import aiogram
from aiogram.utils import executor

from .middleware import CheckUserMiddleware
from .utils import *
from .messages import *


@dp.message_handler(commands=['find_dish'], state='*')
async def find_dish_cmd(message: types.Message):
    await message.answer("Enter your ingredients split by ',' ")
    await FindDishState.enter_ingredients.set()
    await message.delete()


@dp.message_handler(commands=['history'], state='*')
async def check_history_cmd(message: types.Message, state: FSMContext):
    await FindDishState.history.set()
    dishes = filter_dishes(
        db_manager.get_all_user_dishes(message.from_user.id)
    )
    ans = format_dishes_for_message(dishes)
    try:
        await bot.send_message(
            chat_id=message.from_user.id,
            text=ans,
            reply_markup=HistoryKeyboard.generate_kb(dishes),
        )
    except aiogram.utils.exceptions.MessageTextIsEmpty:
        await send_sorry_msg(message.from_user.id)
        await state.reset_state(with_data=False)


@dp.message_handler(commands=['start'], state='*')
async def init_dialog_cmd(message: types.Message, state: FSMContext):
    await state.reset_state(with_data=False)
    await send_welcome_msg(chat_id=message.from_user.id)


test_input = 'nut'


@dp.message_handler(state=FindDishState.enter_ingredients)
async def enter_ingredients(message: types.Message, state: FSMContext):
    ingredients = message.text
    food_searcher.run(test_input)  # TODO
    dishes = food_searcher.get_dishes()
    try:
        async with state.proxy() as data:
            data['dishes'] = dishes
            await FindDishState.show_dishes.set()
            await send_cur_dish_info(data)
    except IndexError:
        await send_sorry_msg(message.from_user.id)
        await state.reset_state(with_data=False)


@dp.callback_query_handler(state=FindDishState.more_info)
async def more_info_callback(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'back':
        await callback.message.delete()
        async with state.proxy() as data:
            await send_cur_dish_info(data)
            await FindDishState.show_dishes.set()
            await callback.answer('back')

    elif callback.data == 'save':
        async with state.proxy() as data:
            dish = get_cur_dish(data)
            user = get_cur_user(data)
            # print(user.tg_id)
            save_dish_event(from_dish_api_repr(dish), user)
            await callback.answer('SAVED!')


@dp.callback_query_handler(state=FindDishState.history)
async def history_callback(callback: types.CallbackQuery, state: FSMContext):
    more_info_prefix = 'dish_'
    if callback.data == 'back':
        await to_start(callback)
        await state.reset_state(with_data=False)

    elif callback.data.startswith(more_info_prefix):
        dish_id = callback.data.removeprefix(more_info_prefix)
        dish = db_manager.get_dish(dish_id)
        await send_dish_info(callback, dish)

    elif callback.data == 'hide':
        await callback.message.delete()

    await callback.answer()


@dp.callback_query_handler(state=FindDishState.show_dishes)
async def dish_list_callback(callback: types.CallbackQuery, state: FSMContext):
    navigation_btns = ['prev', 'next']
    async with state.proxy() as data:
        if callback.data == 'prev':
            prev_dish(data)
        elif callback.data == 'next':
            next_dish(data)
        elif callback.data == 'more':
            await callback.message.delete()
            await send_more_dish_info(callback, dish=get_cur_dish(data))
            await FindDishState.more_info.set()
            await callback.answer()

        elif callback.data == 'stop':
            await to_start(callback)
            await state.reset_state(with_data=False)

        if callback.data in navigation_btns:
            await update_dish_message(callback, dish=get_cur_dish(data))
            await callback.answer()


async def on_startup(_):
    print('RUNNING')


def run():
    dp.middleware.setup(CheckUserMiddleware())
    executor.start_polling(dp, on_startup=on_startup)
