from sqlalchemy import inspect

from db import UserModel, DishModel
from services.dto_models import DishDTO, UserDTO


# Alternatively can create generic mapper, but have to add generic interface for dto


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


class DishMapper:
    def to_sqlalchemy(self, dish_dto: DishDTO) -> DishModel:
        return DishModel(**dish_dto.model_dump())

    def to_dto(self, model: DishModel) -> DishDTO:
        if model is None:
            return None
        return DishDTO.model_validate(object_as_dict(model))


class UserMapper:
    def to_sqlalchemy(self, dto: UserDTO) -> UserModel:
        return UserModel(**dto.model_dump())

    def to_dto(self, model: UserModel) -> UserDTO:
        if model is None:
            return None
        return UserDTO.model_validate(object_as_dict(model))


dish_mapper = DishMapper()
user_mapper = UserMapper()
