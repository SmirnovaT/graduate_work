import pytest

from http import HTTPStatus

from testdata.persons.search_data import (
    persons_search_data,
    persons_search_data_for_pagination,
)

pytestmark = pytest.mark.asyncio

PERSON_ENDPOINT = "persons"


async def test_persons_search_success(make_get_request):
    query = "Scholz"

    status, response = await make_get_request(
        endpoint=PERSON_ENDPOINT + f"/search?query={query}",
    )

    assert status == HTTPStatus.OK
    assert len(response) == 2
    assert response == persons_search_data


async def test_persons_search_not_found(make_get_request):
    query = "Something"

    status, response = await make_get_request(
        endpoint=PERSON_ENDPOINT + f"/search?query={query}",
    )

    assert status == HTTPStatus.OK
    assert len(response) == 0
    assert response == []


async def test_person_search_pagination(make_get_request):
    query = "Kate"
    params = {
        "page_number": 1,
        "page_size": 5,
    }

    status, response = await make_get_request(
        endpoint=PERSON_ENDPOINT + f"/search?query={query}",
        params=params,
    )

    assert status == HTTPStatus.OK
    assert len(response) == params["page_size"]
    assert response == persons_search_data_for_pagination


async def test_person_search_page_number_error(make_get_request):
    query = "Kate"
    params = {
        "page_number": -5,
        "page_size": 5,
    }

    status, response = await make_get_request(
        endpoint=PERSON_ENDPOINT + f"/search?query={query}", params=params,
    )

    assert status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response["detail"][0]["msg"] == "Input should be greater than or equal to 1"


async def test_person_search_page_size_error(make_get_request):
    query = "Kate"
    params = {
        "page_number": 1,
        "page_size": 200,
    }

    status, response = await make_get_request(
        endpoint=PERSON_ENDPOINT + f"/search?query={query}", params=params,
    )

    assert status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response["detail"][0]["msg"] == "Input should be less than or equal to 100"
