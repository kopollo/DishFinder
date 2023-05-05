"""Contain functions that control bot messages."""
import aiogram
from aiogram.utils.exceptions import MessageNotModified
from aiogram import types
from aiogram.dispatcher.storage import FSMContextProxy, FSMContext

from food_api_handler.food_searcher import DishApiRepr
from .markup import HistoryKeyboard, HistoryDishInstructionKeyboard, \
    StartKeyboard, HistoryDishInfoKeyboard, ChooseDishKeyboard, \
    ShowInstructionKeyboard
from .setup import bot, db_manager
from .utils import get_cur_dish, format_dishes_for_message, filter_dishes, \
    get_dishes_to_history, from_dish_api_repr
from db import DishModel


async def send_welcome_msg(chat_id):
    """
    Send welcome msg.

    :param chat_id: chat id where to send a message
    :return: None
    """
    await bot.send_message(
        chat_id=chat_id,
        text='HI HI HI HI',
        reply_markup=StartKeyboard(),
    )


# To implement multi languages better to add param text
async def send_sorry_msg(chat_id):
    """
    Send sorry msg.

    :param chat_id: chat id where to send a message
    :return: None
    """
    await bot.send_message(
        chat_id=chat_id,
        text="I'm sorry but I haven't find anything",
        reply_markup=StartKeyboard(),
    )


async def update_dish_message(callback: types.CallbackQuery, dish: DishApiRepr):
    """
    Update dish message to implement pagination.

    :param callback: callback info from pressed btn
    :param dish: DishApiRepr object
    :return: None
    """
    caption = dish.title + '\n' + '\n' + dish.ingredients
    photo = types.InputMediaPhoto(media=dish.image_url,
                                  caption=caption)
    try:
        await bot.edit_message_media(
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            media=photo,
            reply_markup=ChooseDishKeyboard(),
        )
    except MessageNotModified:
        print('same as before')


async def send_cur_dish_info(data: FSMContextProxy):
    """
    Send current dish from context manager.

    :param data: context manager storage
    :return:
    """
    dish = from_dish_api_repr(get_cur_dish(data))
    await bot.send_photo(
        chat_id=data['chat_id'],
        reply_markup=ChooseDishKeyboard(),
        photo=dish.image_url,
        caption=dish.preview(),
    )


async def send_history_dish_info(callback: types.CallbackQuery,
                                 dish: DishModel) -> None:
    """Send info about dish in history - dish title, ingredients, photo."""
    await callback.message.delete()
    await bot.send_photo(
        chat_id=callback.from_user.id,
        reply_markup=HistoryDishInfoKeyboard(),
        photo=dish.image_url,
        caption=dish.preview(),
    )


async def send_dish_instruction(callback: types.CallbackQuery,
                                dish: DishApiRepr):
    """
    Send message with dish ingredients.

    :param callback: callback info from pressed btn
    :param dish: DishApiRepr
    :return: None
    """
    await callback.message.answer(
        text=dish.instruction,
        reply_markup=ShowInstructionKeyboard(),
    )


async def send_history_widget(user_id: int, state: FSMContext):
    """Send widget with dishes."""
    dishes = get_dishes_to_history(user_id)
    # TODO abort_if_empty_storage except (except statement) much prettier.
    if not len(dishes):
        await send_sorry_msg(user_id)
        await state.reset_state(with_data=False)
    else:
        await bot.send_message(
            chat_id=user_id,
            text=format_dishes_for_message(dishes),
            reply_markup=HistoryKeyboard(dishes),
        )


async def show_instruction_in_history(callback: types.CallbackQuery,
                                      dish: DishApiRepr):
    """Send message with dish instruction."""
    await callback.message.answer(
        text=dish.instruction,
        reply_markup=HistoryDishInstructionKeyboard(),
    )
