from translate import Translator


class LangChecker:
    def __init__(self, user_id: int) -> None:
        self.user_id = user_id

    @staticmethod
    def to_user_lang(text: str) -> str:
        # FULL REFACTOR IT IS TRASH
        translator = Translator(to_lang='en')
        # lang = StoragePort().get_user(user_id).language
        # Looks like better store that info in runtime
        # print(lang)
        lang = 'ruа'
        if lang == 'ru':
            text = translator.translate(text)
        return text

    @staticmethod
    def translate_to(text: str) -> str:
        # Как мне лучше перевести. либо в аргументы функции добавить ещще user
        # id, чтобы проверять внутри, нужно ли переводить, либо в хендлере бота
        # translator = Translator(to_lang=to_lang)
        # return translator.translate(text)
        pass
