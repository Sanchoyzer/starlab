import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient
from aiohttp.web_exceptions import HTTPOk
from yarl import URL


@pytest.fixture
def health_url(app: web.Application) -> URL:
    return app['health_app'].router['health'].url_for()


async def test_health(client: TestClient, health_url: str) -> None:
    response = await client.get(health_url)
    assert response.status == HTTPOk.status_code
    assert (r_json := await response.json()) and 'version' in r_json
