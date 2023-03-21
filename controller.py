from food_api import SearchByIngredientsRequest, GetRecipeInstructionsRequest


class DishApiRepr:
    def __init__(self, title, id, image_url, instruction):
        self.title = title
        self.id = id
        self.image_url = image_url
        self.instruction = instruction

    def __str__(self):
        return f'<Dish> {self.title} {self.image_url}'


class DishBotController:
    def __init__(self):
        self.ingredients = None
        self.dishes = []

        self.answer = []  # RENAME

    def run(self, user_input):
        self.ingredients = user_input
        self.dishes = \
            SearchByIngredientsRequest(self.ingredients).get_all_dishes()
        self.generate_dish_list_for_answer()

    def _info(self):
        for dish in self.dishes:
            print(dish)

    def generate_instruction(self, dish_id):
        instruction = GetRecipeInstructionsRequest(
            dish_id,
        ).get_instruction()

        if instruction is not None:  # CHECK THAT RECIPE is existed
            return self._format_instruction(instruction)
        return None

    def _format_instruction(self, instruction: list):
        formatted_instruction = ""
        for idx, step in enumerate(instruction):
            line = f'{idx + 1}) {step}\n\n'
            formatted_instruction += line
        return formatted_instruction

    def generate_dish_list_for_answer(self):
        for dish in self.dishes:
            title, dish_id, image_url = dish
            instruction = self.generate_instruction(dish_id)
            if instruction is not None:
                dish = DishApiRepr(
                    title=title,
                    id=dish_id,
                    image_url=image_url,
                    instruction=instruction
                )
                print(dish)
                self.answer.append(dish)

    def get_dishes(self):
        return self.answer
