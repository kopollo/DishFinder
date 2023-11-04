"""Contain functions that control bot messages."""
from aiogram.utils.exceptions import MessageNotModified
from .keboards import HistoryKeyboard, HistoryDishInfoKeyboard, ChooseDishKeyboard
from .utils import *
from .msg_templates import *
from services.dto_models import DishDTO


async def update_dish_message(callback: types.CallbackQuery,
                              dish: DishDTO) -> None:
    """
    Update dish message to implement pagination.

    :param callback: callback info from pressed btn
    :param dish: DishInBotRepr object
    :return: None
    """
    user_lang = user_service.get(get_chat_id(callback)).language
    caption = lang_translator.translate(text=dish.preview(), to_lang=user_lang)
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
        pass


async def send_history_dish_info(callback: types.CallbackQuery) -> None:
    """Send info about dish in history - dish title, ingredients, photo."""
    chat_id = get_chat_id(callback)
    state = get_cur_state(chat_id)
    dish = await get_proxy_history_dish(state)
    await send_msg_with_dish(
        update=callback,
        keyboard=HistoryDishInfoKeyboard(),
        dish=dish,
    )


async def send_cur_dish_info(
        update: Union[types.Message, types.CallbackQuery]) -> None:
    """Send current dish in search queue."""
    state = get_cur_state(get_chat_id(update))
    async with state.proxy() as data:
        dish: DishDTO = get_cur_dish(data)
        await send_msg_with_dish(
            update=update,
            keyboard=ChooseDishKeyboard(),
            dish=dish
        )


async def send_history_widget(
        update: Union[types.Message, types.CallbackQuery]) -> None:
    """Send widget with dishes in history."""
    dishes: list[DishDTO] = user_service.get_user_dishes(get_chat_id(update))
    if not dishes:
        await to_start(update=update, text=SORRY)
        return None
    await send_text_msg(
        update=update,
        text=user_service.convert_dishes_list_to_str(dishes),
        keyboard=HistoryKeyboard(dishes),
    )
