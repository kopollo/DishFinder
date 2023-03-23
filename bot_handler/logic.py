from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor

from .setup import *
from .markup import *
from .utils import *


@dp.message_handler(Text(equals='Find dish'))
async def find_dish_event(message: types.Message):
    await message.answer("Enter your ingredients split by ',' ")
    await FindDishState.enter_ingredients.set()
    await message.delete()


@dp.message_handler(Text(equals='History'))
async def check_history_event(message: types.Message, state: FSMContext):
    # TODO
    async with state.proxy() as data:
        db_manager.get_all_user_dishes(get_cur_user(data))
    await message.delete()


@dp.message_handler(commands=['start'])
async def start(message: types.Message, state: FSMContext):
    await bot.send_message(
        chat_id=message.from_user.id,
        text='HI HI HI HI',
        reply_markup=start_kb,
    )
    user = UserModel(tg_id=message.from_user.id)
    db_manager.add_user(user)
    # create a separate function proxy_init()
    async with state.proxy() as data:
        data['chat_id'] = message.from_user.id
        data['cur_dish_id'] = 0
        data['user'] = user


test_input = 'apples,flour,sugar'


@dp.message_handler(state=FindDishState.enter_ingredients)
async def find_dish(message: types.Message, state: FSMContext):
    ingredients = message.text
    controller.run(test_input)
    dishes = controller.get_dishes()
    await message.answer(ingredients)
    try:
        async with state.proxy() as data:
            data['dishes'] = dishes
            await show_cur_dish_info(data)
    except IndexError:  # dont work. need async version???
        print('no dishes')


@dp.callback_query_handler(state=FindDishState.more_info)
async def more_info_state(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        dish: DishApiRepr = get_cur_dish(data)
        user: UserModel = get_cur_user(data)

    if callback.data == 'back':
        await callback.message.delete()
        async with state.proxy() as data:
            await show_cur_dish_info(data)
        await FindDishState.enter_ingredients.set()
        await callback.answer('back')

    elif callback.data == 'save':
        save_dish_event(from_dish_api_repr(dish), user)
        await callback.answer('SAVED!')


@dp.callback_query_handler(state=FindDishState.enter_ingredients)
async def dish_list_keyboard_handler(
        callback: types.CallbackQuery,
        state: FSMContext):
    # don't like - need refactor
    if callback.data == 'prev':
        async with state.proxy() as data:
            prev_dish(data)
            dish = get_cur_dish(data)
            await update_dish_message(callback, dish)
            await callback.answer('prev')

    elif callback.data == 'next':
        async with state.proxy() as data:
            next_dish(data)
            dish = get_cur_dish(data)
            await update_dish_message(callback, dish)
            await callback.answer('next')

    elif callback.data == 'more':
        await callback.message.delete()
        async with state.proxy() as data:
            dish = get_cur_dish(data)
            await callback.message.answer(
                text=dish.instruction,
                reply_markup=more_kb,
            )
        await FindDishState.more_info.set()
        await callback.answer()

    elif callback.data == 'stop':
        await to_start(callback)
        await state.reset_state(with_data=False)


async def on_startup(_):
    print('RUNNING')


def run():
    executor.start_polling(dp, on_startup=on_startup)
