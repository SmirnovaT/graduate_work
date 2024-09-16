from http import HTTPStatus

import pytest

from src.tests.functional.settings import test_settings
from src.tests.functional.test_data.vk import data_vk


@pytest.mark.asyncio
async def test_assistant_vk_success(client_session, make_post_request):
    status, response = await make_post_request(test_settings.api_vk, data_vk)
    assert status == HTTPStatus.OK


async def test_assistant_yandex_success(client_session, make_post_request):
    status, response = await make_post_request(test_settings.api_vk, data_vk)
    assert status == HTTPStatus.OK
