"""Contain middlewares."""
from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from services.dto_models import UserDTO
from .utils import init_fsm_proxy, get_chat_id, get_cur_state, init_user_by_update
from .setup import user_service


class CheckUserMiddleware(BaseMiddleware):
    """Checks user existence in db, init runtime storage for user."""

    async def on_pre_process_update(self, full_update: types.Update,
                                    data: dict):
        """Check msg and callback data before handlers."""
        update = full_update.message
        if not update:
            update = full_update.callback_query
        user_id = get_chat_id(update)
        state = get_cur_state(user_id)
        async with state.proxy() as data:
            if not data:
                user: UserDTO = init_user_by_update(update)
                if not user_service.get(user_id):
                    # print('XXXXXXXXXX')
                    # print()
                    user_service.save(user)
                to_store = {
                    'chat_id': user_id,
                    'cur_dish_id': 0,
                    'user': user
                }
                await init_fsm_proxy(state, to_store)
