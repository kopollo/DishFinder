from dataclasses import asdict
from typing import Optional

from bot.context import DishInBotRepr, TelegramUser
from bot.services.storage_port import BaseStorage
from db import DishModel, UserModel
import db.crud_wrappers as db_manager


class DBAdapter(BaseStorage):

    def _to_dish_in_bot_repr(self, dish: DishModel) -> DishInBotRepr:
        dish_repr = DishInBotRepr(
            id=dish.id,
            title=dish.title,
            image_url=dish.image_url,
            ingredients=dish.ingredients,
            instruction=dish.instruction,
        )
        return dish_repr

    def _to_user_model(self, tg_user: TelegramUser) -> Optional[UserModel]:
        return UserModel(**asdict(tg_user))

    def _to_telegram_user(self, user_model: UserModel) -> TelegramUser:
        # TODO write to_dict for DB models
        user = TelegramUser(
            first_name=user_model.first_name,
            last_name=user_model.last_name,
            tg_id=user_model.tg_id,
            language=user_model.language,
        )
        return user

    def _to_dish_model(self, dish: DishInBotRepr) -> DishModel:
        dish_repr = DishModel(**asdict(dish))
        return dish_repr

    def get_dish(self, dish_id: int) -> DishInBotRepr:
        """Return dish from DB by id."""
        return self._to_dish_in_bot_repr(db_manager.get_dish(dish_id))

    def save_dish(self, dish: DishInBotRepr, user: TelegramUser) -> None:
        """Save a dish to user in DB."""
        db_manager.save_dish_event(self._to_dish_model(dish),
                                   self._to_user_model(user))

    def get_user_dishes(self, user_id: int) -> list[DishInBotRepr]:
        """Return dishes in DB by user id."""
        dishes = db_manager.get_all_user_dishes(user_id)
        dishes = [self._to_dish_in_bot_repr(i) for i in dishes]
        return dishes

    def add_user(self, user: TelegramUser) -> None:
        """Add user to DB."""
        db_manager.add_user(self._to_user_model(user))

    def get_user(self, user_id) -> Optional[TelegramUser]:
        """Return user in DB, if user exist and None otherwise."""
        user_model = db_manager.get_user(user_id)
        if not user_model:
            return None
        return self._to_telegram_user(user_model)

    def set_user_lang(self, user_id: int, lang: str) -> None:
        try:
            db_manager.set_user_lang(user_id=user_id, lang=lang)
        except Exception:
            print('cant set lang to user')
