from dataclasses import asdict
from typing import Optional
from ..bot_context import DishInBotRepr, TelegramUser
# from db.adapter import db_adapter as adapter
from abc import ABC, abstractmethod


class BaseStorage(ABC):
    @abstractmethod
    def get_dish(self, dish_id: int) -> DishInBotRepr:
        """Return a dish in DB by id and convert it to DishInBotRepr."""

    @abstractmethod
    def save_dish(self, dish: DishInBotRepr, user: TelegramUser) -> None:
        """Save a dish to user in DB."""

    @abstractmethod
    def get_user_dishes(self, user_id: int) -> list[DishInBotRepr]:
        """Return dishes in DB by user id."""

    @abstractmethod
    def add_user(self, user: TelegramUser) -> None:
        """Add user to DB."""

    @abstractmethod
    def get_user(self, user_id: int) -> Optional[TelegramUser]:
        """Return user in DB, if user exist and None otherwise."""

    @abstractmethod
    def set_user_lang(self, user_id: int, lang: str) -> None:
        """Return user in DB, if user exist and None otherwise."""
