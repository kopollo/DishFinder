from dataclasses import dataclass

from pydantic import BaseModel, Field, AliasChoices


class DishDTO(BaseModel):
    title: str
    id: int
    image_url: str = Field(validation_alias=AliasChoices('image', 'image_url'))
    ingredients: str = ""
    instruction: str = ""

    def preview(self):
        return self.title + '\n' + '\n' + self.ingredients


class UserDTO(BaseModel):
    tg_id: int
    first_name: str
    last_name: str
    language: str = "en"
