from db.repositories import DishRepository
from services.dto_models import DishDTO


class DishService:
    def __init__(self, repository: DishRepository):
        self.repository = repository

    def get(self, idx: int):
        return self.repository.get(idx)

    def save(self, dish: DishDTO):
        self.repository.save(dish)

    @staticmethod
    def bound(dishes: list[DishDTO]) -> list[DishDTO]:
        """Limit the number of dishes shown to the user to 10."""
        return dishes[:10]

    @staticmethod
    def to_message_format(dishes: list[DishDTO]) -> str:
        """
        Format dishes for bot message to show user.

        :param dishes: list of dishes
        :return: str
        """
        ans = ''
        for i, dish in enumerate(dishes):
            ans += f'{i}) {dish.title}\n'
        return ans

    def get_formatted_dishes(self, dishes: list[DishDTO]):
        # user_repository.get_all_user_dishes(user_id)
        return self.to_message_format(self.bound(dishes))

