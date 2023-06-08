"""Contain message and callback handlers."""
from aiogram.utils import executor

from .bot_context import FindDishState
from .middleware import CheckUserMiddleware
from .messages import *
from .msg_templates import *
from .keboards import *
from .setup import db_manager
import bot_handler.services.dish_search_port as dish_search


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
    Handle /start command that send welcome msg.

    :param message: input msg from user
    :param state: position in the final state machine
    :return: None
    """
    await to_start(update=message, text=START)


@dp.message_handler(commands=['settings'], state='*')
async def settings_cmd(message: types.Message):
    """Handle /settings command."""
    await FindDishState.settings.set()
    await send_text_msg(
        update=message,
        text=SETTINGS,
        keyboard=SettingsKeyboard(),
    )


@dp.message_handler(state=FindDishState.enter_ingredients)
async def enter_ingredients(message: types.Message, state: FSMContext):
    """
    Handle user input ingredients and call food api to get list of dishes.

    :param message: input msg from user
    :param state: position in the final state machine
    :return: None
    """
    ingredients: str = message.text
    ingredients = LangChecker(get_chat_id(message)).to_eng(ingredients)
    dishes = dish_search.get_dishes(ingredients)
    logging.info(ingredients + " " + str(message.from_user.id))
    # CAN be replaced in utils as save_dishes_if_exist() to separate logic
    if not dishes:
        await to_start(update=message, text=SORRY)
        return None
    async with state.proxy() as data:
        data['dishes'] = dishes
        data['cur_dish_id'] = 0
    await FindDishState.show_dishes.set()
    await send_cur_dish_info(message)


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
            dish: DishInBotRepr = get_cur_dish(data)
            user: TelegramUser = get_cur_user(data)
            #  maybe user.save_dish(dish) ?
            db_manager.save_dish(dish=dish, user=user)
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
        await to_start(update=callback, text=START)
        await callback.message.delete()

    elif callback.data.startswith(more_info_prefix):
        dish_id = int(callback.data.removeprefix(more_info_prefix))
        dish: DishInBotRepr = db_manager.get_dish(dish_id)

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
                keyboard=ShowInstructionInSearchKeyboard())

        elif callback.data == 'stop':
            await to_start(update=callback, text=START)

        if callback.data in navigation_btns:
            await update_dish_message(callback, dish=get_cur_dish(data))
        await callback.answer()


@dp.callback_query_handler(state=FindDishState.settings)
async def settings_callback(
        callback: types.CallbackQuery, state: FSMContext):
    """Handle callback data in SettingsKeyboard."""
    lang = "en"
    if callback.data == 'ru':
        lang = "ru"
    db_manager.set_user_lang(get_chat_id(callback), lang=lang)
    await callback.message.delete()
    await to_start(update=callback, text=START)


def run():
    """Register middleware and start polling bot."""
    dp.middleware.setup(CheckUserMiddleware())
    executor.start_polling(dp)
