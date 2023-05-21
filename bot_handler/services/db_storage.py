from dataclasses import asdict
from typing import Optional
from ..bot_context import DishInBotRepr, TelegramUser
from db.adapter import db_adapter as adapter


def get_dish( dish_id: int) -> DishInBotRepr:
    """Return a dish in DB by id and convert it to DishInBotRepr."""
    return adapter.get_dish(dish_id)


def save_dish( dish: DishInBotRepr, user: TelegramUser) -> None:
    """Save a dish to user in DB."""
    return adapter.save_dish(dish, user)


def get_user_dishes(user_id: int) -> list[DishInBotRepr]:
    """Return dishes in DB by user id."""
    return adapter.get_user_dishes(user_id)


def add_user(user: TelegramUser) -> None:
    """Add user to DB."""
    adapter.add_user(user)


def get_user(user_id: int) -> Optional[TelegramUser]:
    """Return user in DB, if user exist and None otherwise."""
    return adapter.get_user(user_id)


def set_user_lang(user_id: int, lang: str) -> None:
    """Return user in DB, if user exist and None otherwise."""
    adapter.set_user_lang(user_id=user_id, lang=lang)
