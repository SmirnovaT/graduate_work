from http import HTTPStatus

from langchain.tools import tool

from src.services.giga_chat_service.helper_functions import (
    get_similar,
    get_film,
    get_film_by_uuid,
    get_person,
    format_film_info,
    get_person_list,
)
from src.utils.translate_text import translate_if_russian


@tool(return_direct=True, response_format="content_and_artifact", parse_docstring=True)
def get_films_by_person(person_name: str) -> tuple[str, list | None]:
    """
    Функция по имени актера возвращает названия фильмов, в которых он снимался.

    Args:
        person_name: Имя человека, о котором нужно найти информацию.

    Returns:
        title (list[str]): названия фильмов
    """

    person_name = translate_if_russian(person_name)
    person_list = get_person(person_name)
    if len(person_list) > 0:
        films_uuid = person_list[0]["films"]

        films = []
        # Читаемость кода здесь важнее, чем демонстрация list comprehension
        for film_uuid in films_uuid:
            film = get_film_by_uuid(film_uuid["uuid"])
            films.append(film["title"])

        return f"Фильмы с участием {person_name}:\n{'\n'.join(films)}", films
    return f"Фильм c персоной: {person_name} не найден", None


@tool(return_direct=True, response_format="content_and_artifact", parse_docstring=True)
def get_actors_from_film(film_title: str) -> tuple[str, list | None]:
    """
    Функция по названию фильма возвращает список актеров, которые снимались в фильме.

    Args:
        film_title: название фильма, по которому ведётся поиск

    Returns:
        list[str]: Список актеров фильма
        str: В случае ошибки возвращает строку с сообщением об ошибке.
    """

    return get_person_list(film_title, person_type="actors")


@tool(return_direct=True, response_format="content_and_artifact", parse_docstring=True)
def get_writers_from_film(film_title: str) -> tuple[str, list | None]:
    """
    Функция по названию фильма возвращает список сценаристов (авторов) фильма,
    которые придумали фильм.

    Args:
        film_title: название фильма, по которому ведётся поиск

    Returns:
        list[str]: Список сценаристов (авторов) фильма
        str: В случае ошибки возвращает строку с сообщением об ошибке.
    """

    return get_person_list(film_title, person_type="writers")


@tool(return_direct=True, response_format="content_and_artifact", parse_docstring=True)
def get_directors_from_film(film_title: str) -> tuple[str, list | None]:
    """
    Функция по названию фильма возвращает список режиссеров фильма.

    Args:
        film_title: название фильма, по которому ведётся поиск

    Returns:
        list[str]: Список режиссеров фильма
        str: В случае ошибки возвращает строку с сообщением об ошибке.
    """

    return get_person_list(film_title, person_type="directors")


@tool(return_direct=True, response_format="content_and_artifact", parse_docstring=True)
def get_film_rating(film_title: str) -> tuple[str, dict | None]:
    """Функция по названию фильма возвращает рейтинг фильма.

    Args:
       film_title: Название фильма

    Returns:
       Int: рейтинг фильмов
    """

    film_title = translate_if_russian(film_title)
    film, status_code = get_film(film_title)

    if status_code == HTTPStatus.OK:
        rating = film[0]["imdb_rating"]
        return f"Рейтинг фильма: {rating}", rating
    return f"Фильм c названием {film_title} не найден", None


@tool(return_direct=True, response_format="content_and_artifact", parse_docstring=True)
def get_full_film_info(film_title: str) -> tuple[str, dict | None]:
    """Функция возвращает полную информацию о фильме.
    Возвращает пользователю название, описание, рейтинг, жанр,
    актеров, авторов (сценаристов) и режиссеров.

    Args:
        film_title: Название фильма

    Returns:
          dict: Описание фильма
    """

    film_title = translate_if_russian(film_title)
    film, status_code = get_film(film_title)
    if status_code == HTTPStatus.OK:
        film_uuid = film[0]["uuid"]
        full_info_film = get_film_by_uuid(film_uuid)
        description = format_film_info(full_info_film)
        return description, full_info_film
    return "Фильм не найден", None


@tool(return_direct=True, response_format="content_and_artifact", parse_docstring=True)
def get_similar_films(film_title: str) -> tuple[str, list[str] | None]:
    """Функция ищет похожие фильмы.
    Отвечает на запрос пользователя найти похожие фильмы

    Args:
        film_title: Название фильма

    Returns:
          list[dict]: похожие фильмы
    """

    film_title = translate_if_russian(film_title)

    film, status_code = get_film(film_title)
    if status_code == HTTPStatus.OK:
        film_uuid = film[0]["uuid"]
        similar_films = get_similar(film_uuid)
        films = []
        for similar_film in similar_films:
            films.append(similar_film["title"])
        return f"Похожие фильмы: {films}", films
    return f"Фильм c названием {film_title} не найден", None


tools = [
    get_films_by_person,
    get_film_rating,
    get_full_film_info,
    get_similar_films,
    get_actors_from_film,
    get_writers_from_film,
    get_directors_from_film,
]
