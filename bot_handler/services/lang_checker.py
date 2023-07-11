"""Language translator (later going to be an interface)."""
from translate import Translator
from ..setup import db_manager


class BaseTranslator:
    """Lang checker and translator."""

    def _should_proceed(self) -> bool:
        """Check if text should be processed."""

    def to_user_lang(self, text: str) -> str:
        """Translate text to user lang that was _init_."""

    def to_eng(self, text: str) -> str:
        """Translate text from ru to eng."""
