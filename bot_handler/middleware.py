"""Contain middlewares."""
from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from bot_handler.setup import db_manager, dp
from bot_handler.utils import init_fsm_proxy, get_chat_id, get_cur_state
from db import UserModel


class CheckUserMiddleware(BaseMiddleware):
    """Checks user existence in db, init runtime storage for user."""

    async def on_pre_process_update(self, update: types.Update, data: dict):
        """Check msg and callback data before handlers."""
        if update.message:
            user_id = get_chat_id(update.message)
        else:
            user_id = get_chat_id(update.callback_query)

        if not db_manager.is_user_exist(user_id):
            user = UserModel(tg_id=user_id)
            db_manager.add_user(user)
        state = get_cur_state(user_id)
        async with state.proxy() as data:
            if not data:
                to_store = {
                    'chat_id': user_id,
                    'cur_dish_id': 0,
                    'user': db_manager.get_user(user_id)
                }
                await init_fsm_proxy(state, to_store)
