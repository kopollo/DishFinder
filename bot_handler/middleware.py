"""Contain middlewares."""
from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

# from bot_handler.setup import db_filter, dp
from bot_handler.utils import init_fsm_proxy, get_chat_id, get_cur_state, \
    init_user_model
from .setup import db_filter


class CheckUserMiddleware(BaseMiddleware):
    """Checks user existence in db, init runtime storage for user."""

    async def on_pre_process_update(self, full_update: types.Update,
                                    data: dict):
        """Check msg and callback data before handlers."""
        update = full_update.message
        if not update:
            update = full_update.callback_query
        user_id = get_chat_id(update)

        if not db_filter.get_user(user_id):
            user = init_user_model(update)
            db_filter.add_user(user)
        state = get_cur_state(user_id)
        async with state.proxy() as data:
            if not data:
                to_store = {
                    'chat_id': user_id,
                    'cur_dish_id': 0,
                    'user': db_filter.get_user(user_id)
                }
                await init_fsm_proxy(state, to_store)
