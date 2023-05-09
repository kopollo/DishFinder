"""Contain message and callback handlers."""
from aiogram.utils import executor

from .markup import FindDishState
from .middleware import CheckUserMiddleware
from .setup import *
from .utils import *
from .messages import *
from food_api_handler.food_searcher import FoodApiManager
from .msg_templates import START, ENTER, SORRY


@dp.message_handler(commands=['find_dish'], state='*')
async def find_dish_cmd(message: types.Message):
    """
    Handle /find_dish command, that set state to enter ingredients..

    :param message: input msg from user
    :return: None
    """
    await send_text_msg(update=message, text=ENTER, )
    await FindDishState.enter_ingredients.set()
    await message.delete()


@dp.message_handler(commands=['history'], state='*')
async def check_history_cmd(message: types.Message, state: FSMContext):
    """
    Handle /history command, that send to user saved dishes.

    :param message: input msg from user
    :param state: position in the final state machine
    :return: None
    """
    await FindDishState.history.set()
    await send_history_widget(message)


@dp.message_handler(commands=['start'], state='*')
async def init_dialog_cmd(message: types.Message, state: FSMContext):
    """
    Handle /start command, that send welcome msg.

    :param message: input msg from user
    :param state: position in the final state machine
    :return: None
    """
    await to_start(message, state)


@dp.message_handler(state=FindDishState.enter_ingredients)
async def enter_ingredients(message: types.Message, state: FSMContext):
    """
    Handle user input ingredients and call food api to get list of dishes.

    :param message: input msg from user
    :param state: position in the final state machine
    :return: None
    """
    ingredients = message.text
    dishes = FoodApiManager(ingredients).get_dishes()
    try:
        async with state.proxy() as data:
            data['dishes'] = dishes
            data['cur_dish_id'] = 0
        await FindDishState.show_dishes.set()
        await send_cur_dish_info(message)
    except IndexError:
        await to_start(message, state)


@dp.callback_query_handler(state=FindDishState.show_instruction)
async def show_instruction_in_search_callback(callback: types.CallbackQuery,
                                              state: FSMContext):
    """
    Handle callback data in MoreInfoKeyboard.

    :param callback: callback info from pressed btn
    :param state: position in the final state machine
    :return: None
    """
    if callback.data == 'back':
        await send_cur_dish_info(callback)
        await FindDishState.show_dishes.set()
        await callback.message.delete()
        await callback.answer('back')

    elif callback.data == 'save':
        async with state.proxy() as data:
            dish: DishModel = get_cur_dish(data)
            user = get_cur_user(data)
            db_manager.save_dish_event(dish, user)
            await callback.answer('SAVED!')


@dp.callback_query_handler(state=FindDishState.history)
async def history_callback(callback: types.CallbackQuery, state: FSMContext):
    """
    Handle callback data in HistoryKeyboard.

    :param callback: callback info from pressed btn
    :param state: position in the final state machine
    :return: None
    """
    more_info_prefix = 'dish_'
    if callback.data == 'back':
        await to_start(callback, state)
        await callback.message.delete()

    elif callback.data.startswith(more_info_prefix):
        dish_id = int(callback.data.removeprefix(more_info_prefix))
        dish: DishModel = db_manager.get_dish(dish_id)

        await save_history_dish_in_proxy(dish=dish, state=state)
        await FindDishState.show_history_dish.set()
        await send_history_dish_info(callback)
        await callback.message.delete()
    await callback.answer()


@dp.callback_query_handler(state=FindDishState.show_history_dish)
async def show_dish_in_history(callback: types.CallbackQuery,
                               state: FSMContext):
    """
    Handle callback data in HistoryDishInfoKeyboard.

    :param callback: callback info from pressed btn
    :param state: position in the final state machine
    :return: None
    """
    if callback.data == 'back':
        await FindDishState.history.set()
        await callback.message.delete()
        await send_history_widget(callback)

    elif callback.data == 'show_instruction':
        dish = await get_proxy_history_dish(state)
        await FindDishState.history_show_instruction.set()
        await callback.message.delete()
        await send_text_msg(
            update=callback,
            text=dish.instruction,
            keyboard=HistoryDishInstructionKeyboard(),
        )

    await callback.answer()


@dp.callback_query_handler(state=FindDishState.history_show_instruction)
async def show_dish_instruction_in_history(callback: types.CallbackQuery):
    """
    Handle callback data in HistoryDishInstructionKeyboard.

    :param callback: callback info from pressed btn
    :return: None
    """
    if callback.data == 'back':
        await FindDishState.show_history_dish.set()
        await callback.message.delete()
        await send_history_dish_info(callback)


@dp.callback_query_handler(state=FindDishState.show_dishes)
async def dish_list_in_search_callback(
        callback: types.CallbackQuery, state: FSMContext):
    """
    Handle callback data in ChooseDishKeyboard.

    :param callback: callback info from pressed btn
    :param state: position in the final state machine
    :return: None
    """
    navigation_btns = ['prev', 'next']
    async with state.proxy() as data:
        if callback.data == 'prev':
            prev_dish(data)
        elif callback.data == 'next':
            next_dish(data)
        elif callback.data == 'more':
            await FindDishState.show_instruction.set()
            await callback.message.delete()
            await send_text_msg(
                update=callback,
                text=get_cur_dish(data).instruction,
                keyboard=ShowInstructionKeyboard())

        elif callback.data == 'stop':
            await to_start(callback, state)

        if callback.data in navigation_btns:
            await update_dish_message(callback, dish=get_cur_dish(data))
        await callback.answer()


def run():
    """Register middleware and start polling bot."""
    dp.middleware.setup(CheckUserMiddleware())
    executor.start_polling(dp)
