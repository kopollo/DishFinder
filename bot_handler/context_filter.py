from dataclasses import asdict

from bot_handler.markup import DishInBotRepr
from db.db_manager import DBManager
from db import DishModel, UserModel

db_manager = DBManager()


class DBFilter:
    def to_dish_in_bot_repr(self, dish: DishModel) -> DishInBotRepr:
        dish_repr = DishInBotRepr(
            image_url=dish.image_url,
            title=dish.title,
            id=dish.id,
            ingredients=dish.instruction,
            instruction=dish.instruction,
        )
        return dish_repr

    def to_dish_model(self, dish: DishInBotRepr) -> DishModel:
        dish_repr = DishModel(**asdict(dish))
        return dish_repr

    def get_dish(self, dish_id: int) -> DishInBotRepr:
        return self.to_dish_in_bot_repr(db_manager.get_dish(dish_id))

    def save_dish(self, dish: DishInBotRepr, user: UserModel) -> None:
        db_manager.save_dish_event(self.to_dish_model(dish), user)
        #  dont forget also to bound user

    def get_user_dishes(self, user_id: int) -> list[DishInBotRepr]:
        dishes = db_manager.get_all_user_dishes(user_id)
        dishes = [self.to_dish_in_bot_repr(i) for i in dishes]
        return dishes

    def add_user(self, user: UserModel) -> None:
        db_manager.add_user(user)

    def get_user(self, user_id) -> UserModel:
        return db_manager.get_user(user_id)
