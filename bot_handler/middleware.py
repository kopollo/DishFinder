from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from bot_handler.setup import db_manager, dp
from bot_handler.utils import init_fsm_proxy


class CheckUserMiddleware(BaseMiddleware):

    async def on_pre_process_update(self, update: types.Update, data: dict):
        try:
            user_id = update.message.from_user.id
            chat_id = update.message.chat.id
        except AttributeError:
            user_id = update.callback_query.message.from_user.id
            chat_id = update.callback_query.message.chat.id

        state = dp.current_state(chat=chat_id, user=user_id)
        async with state.proxy() as data:
            if not data:
                to_store = {
                    'chat_id': chat_id,
                    'cur_dish_id': 0,
                    'user': db_manager.get_user(user_id)
                }
                await init_fsm_proxy(state, to_store)
