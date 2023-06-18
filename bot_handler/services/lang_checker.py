"""Language translator (later going to be an interface)."""
from translate import Translator
from ..setup import db_manager


class LangChecker:
    """Lang checker and translator."""

    def __init__(self, user_id: int) -> None:
        """
        Init user language.

        :param user_id: user_id in storage
        """
        self.lang = db_manager.get_user(user_id).language
        # Looks like better store that info in runtime

    def _should_proceed(self) -> bool:
        """Check if text should be processed."""
        if self.lang == 'en':
            return False
        return True

    def to_user_lang(self, text: str) -> str:
        """Translate text to user lang that was _init_."""
        if not self._should_proceed():
            return text
        translator = Translator(self.lang)
        text = translator.translate(text)
        return text

    def to_eng(self, text: str) -> str:
        """Translate text from ru to eng."""
        if self._should_proceed():
            translator = Translator(to_lang='en', from_lang='ru')
            return translator.translate(text)
        return text
