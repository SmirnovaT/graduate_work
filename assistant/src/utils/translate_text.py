import translate

from src.core.logger import assistant_logger


def translate_if_russian(title: str) -> str:
    """
    Переводит название на английский, если оно на русском.
    В противном случае, возвращает название без изменений.
    """

    try:
        translator = translate.Translator(from_lang="ru", to_lang="en")
        return translator.translate(title)
    except Exception as e:
        assistant_logger.error(e)
        return title
