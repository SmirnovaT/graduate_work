from http import HTTPStatus
from uuid import UUID

import httpx

from src.core.config import settings
from src.utils.cache import RedisCacheService, get_redis
from src.utils.translate_text import translate_if_russian

cache = RedisCacheService(get_redis())


def get_person(person_name: str) -> tuple:
    """Получение персоны из сервиса movies полнотекстовым поиском."""

    response = httpx.get(
        f"{settings.api_persons}/search",
        params={"query": person_name, "page_size": 1, "page_number": 1},
    )
    return response.json()


def get_film(film_title: str) -> tuple:
    """Получение фильма из сервиса movies полнотекстовым поиском."""

    response = httpx.get(
        f"{settings.api_films}/search/",
        params={"search": film_title, "page_size": 1, "page_number": 1},
    )
    return response.json(), response.status_code


@cache.cached
def get_film_by_uuid(film_uuid: UUID) -> dict:
    """Получение полной информации о фильме из сервиса movies по UUID."""

    response = httpx.get(f"{settings.api_films}/{film_uuid}")
    return response.json()


@cache.cached
def get_similar(film_uuid: UUID) -> dict:
    """Получение похожих фильмов из сервиса movies."""
    response = httpx.get(f"{settings.api_films}/{film_uuid}/similar")
    return response.json()


def format_film_info(full_info_film: dict) -> str:
    """Форматирует информацию о фильме для вывода пользователю."""

    description = f"Название: {full_info_film['title']}\n"
    description += f"Описание: {full_info_film['description']}\n"
    description += f"Рейтинг: {full_info_film['imdb_rating']}\n"
    description += format_person_list("Актеры", full_info_film.get("actors", []))
    description += format_person_list("Сценаристы", full_info_film.get("writers", []))
    description += format_person_list("Режиссеры", full_info_film.get("directors", []))
    return description


def format_person_list(title: str, people: list) -> str:
    """Форматирует список людей (актеров, сценаристов, режиссеров)
    для вывода пользователю."""

    if people:
        names = [person["full_name"] for person in people]
        return f"{title} фильма: {', '.join(names)}\n"
    return f"Про {title.lower()} данного фильма, к сожалению, мне неизвестно\n"


def format_message_for_person_type(
    film_title: str, list_people: list, person_type: str
) -> tuple[str, list]:
    """
    Формирует сообщение для пользователя в зависимости от типа людей.
    """
    person_types = {
        "directors": "Режиссеры фильма {film_title}: {persons}",
        "writers": "Фильм {film_title} придумали сценаристы {persons}",
        "actors": "В фильме {film_title} снимались актеры: {persons}",
    }

    return person_types.get(person_type).format(film_title=film_title, persons=", ".join(list_people)), list_people 


def get_person_list(film_title: str, person_type: str) -> tuple[str, list | None]:
    """
    Функция получения списка актеров, режиссеров или авторов фильма.
    """

    film_title = translate_if_russian(film_title)

    film, status_code = get_film(film_title)
    if status_code == HTTPStatus.OK:
        film_uuid = film[0]["uuid"]
        full_film_info = get_film_by_uuid(film_uuid)

        persons = full_film_info[person_type]
        if persons:
            list_persons = []
            for person in persons:
                list_persons.append(person["full_name"])
            return format_message_for_person_type(film_title, list_persons, person_type)
        return "К сожалению, у меня нет такой информации", None
    return f"Ошибка при получении информации о фильме: {film_title}", None
