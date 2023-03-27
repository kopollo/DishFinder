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
    history_kb = InlineKeyboardMarkup()
    back_btn = InlineKeyboardButton(
        text='back',
        callback_data='back'
    )
    history_kb.add(back_btn)
    # need to be generated every time -> relocate to new def()
    await FindDishState.history.set()
    async with state.proxy() as data:
        dishes = db_manager.get_all_user_dishes(get_cur_user(data))
        ans = format_dishes_for_message(dishes)
        await bot.send_message(
            chat_id=message.from_user.id,
            text=ans,
            reply_markup=history_kb,
        )


@dp.message_handler(commands=['start'])
async def start(message: types.Message, state: FSMContext):
    # SPLIT INTO start with storage init+start_state_set() and
    # start that sends message, then refactor to_start()
    await bot.send_message(
        chat_id=message.from_user.id,
        text='HI HI HI HI',
        reply_markup=start_kb,
    )
    user = UserModel(tg_id=message.from_user.id)  # make init_user_in_db()
    db_manager.add_user(user)
    to_store = {
        'chat_id': message.from_user.id,
        'cur_dish_id': 0,
        'user': user,
    }
    await init_fsm_proxy(state, to_store)


test_input = 'apples,flour,sugar'


@dp.message_handler(state=FindDishState.enter_ingredients)
async def find_dishes(message: types.Message, state: FSMContext):
    ingredients = message.text
    food_searcher.run(test_input)
    dishes = food_searcher.get_dishes()
    await message.answer(ingredients)
    try:
        async with state.proxy() as data:
            data['dishes'] = dishes
            await show_cur_dish_info(data)
    except IndexError:  # dont work. need async version???
        print('no dishes')


@dp.callback_query_handler(state=FindDishState.more_info)
async def show_more_dish_info(callback: types.CallbackQuery, state: FSMContext):
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


@dp.callback_query_handler(state=FindDishState.history)
async def history_callback(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'back':
        await to_start(callback)
        await state.reset_state(with_data=False)


@dp.callback_query_handler(state=FindDishState.enter_ingredients)
async def dish_list_callback(callback: types.CallbackQuery, state: FSMContext):
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
