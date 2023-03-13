from food_api import SearchByIngredientsRequest, GetRecipeInstructionsRequest

d = 'apples,flour,sugar'


class DishBotController:
    def __init__(self):
        self.ingredients = None
        self.dishes = []

        self.answer = []  # RENAME

    def run(self, user_input):
        self.ingredients = user_input
        self.dishes = SearchByIngredientsRequest(d).get_all_dishes()
        self.generate_dish_list_for_answer()
        # CHANGE d INTO USER INPUT

    def info(self):
        for line in self.answer:
            print(line['image_url'])

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
            line = f'{idx}) {step}\n'
            formatted_instruction += line
        return formatted_instruction

    def generate_dish_list_for_answer(self):
        for dish in self.dishes:
            title, dish_id, image_url = dish
            instruction = self.generate_instruction(dish_id)
            if instruction is not None:
                dish_info = {
                    'title': title,
                    'dish_id': dish_id,
                    'image_url': image_url,
                    'instruction': instruction,
                }
                self.answer.append(dish_info)
