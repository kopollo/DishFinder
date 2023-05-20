from translate import Translator
from ..services.db_storage import get_user


class LangChecker:
    def __init__(self, user_id: int) -> None:
        self.lang = get_user(user_id).language
        # Looks like better store that info in runtime

    def _should_proceed(self) -> bool:
        if self.lang == 'en':
            return False
        return True

    def to_user_lang(self, text: str) -> str:
        if not self._should_proceed():
            return text
        translator = Translator(self.lang)
        text = translator.translate(text)
        return text

    def to_eng(self, text: str) -> str:
        if self._should_proceed():
            translator = Translator(to_lang='en', from_lang='ru')
            return translator.translate(text)
        return text
