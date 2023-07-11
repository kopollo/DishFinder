"""Language translator service"""
from bot_handler.services.lang_checker import BaseTranslator


class LangTranslator(BaseTranslator):
    """Language and translator."""

    def __init__(self, lang: str) -> None:
        """Init with user language."""
        self.lang = lang

    def _should_proceed(self) -> bool:
        """Check if text should be processed."""
        if self.lang == 'en':
            return False
        return True

    def to_user_lang(self, text: str) -> str:
        """Translate text to user lang that was _init_."""
        if not self._should_proceed():
            return text

        # translator = Translator(self.lang)
        # text = translator.translate(text)
        return text

    # def to_eng(self, text: str) -> str:
    #     """Translate text from ru to eng."""
    #     if self._should_proceed():
    #         translator = Translator(to_lang='en', from_lang='ru')
    #         return translator.translate(text)
    #     return text

    def translate(self, text):
        pass
        # Нужно обобщить - сделать функцию


def translate_request(text: str, from_lang: str, to_lang: str):
    url = "https://api.mymemory.translated.net/get"
    params = {
        "q": text,
        "langpair": f'{from_lang}|{to_lang}'
    }
    print()
