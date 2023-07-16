"""Language translator service"""
import re

from web_utils import get_request


class LangTranslator:
    """Language and translator."""

    def translate(self, text: str, to_lang: str) -> str:
        from_lang: str = get_text_lang(text)
        if from_lang != to_lang:
            text = translate_request(text, from_lang, to_lang)
        return text


def translate_request(text: str, from_lang: str, to_lang: str) -> str:
    url = "https://api.mymemory.translated.net/get"
    params = {
        "q": text,
        "langpair": f'{from_lang}|{to_lang}'
    }
    res = get_request(url, params=params)
    ans = res.json()['responseData']['translatedText']
    # print(get_text_lang(text))
    # print(ans)
    return ans


def get_text_lang(text: str) -> str:
    if bool(re.search('[а-яА-Я]', text)):
        return 'ru'
    return 'en'
