import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient
from aiohttp.web_exceptions import HTTPBadRequest, HTTPCreated
from faker import Faker
from yarl import URL


@pytest.fixture
def books_url(app: web.Application) -> URL:
    return app['library_app'].router['books'].url_for()


async def test_books_post(client: TestClient, books_url: str, book_creation_data: dict) -> None:
    response = await client.post(books_url, json=book_creation_data)
    assert response.status == HTTPCreated.status_code
    assert (r_json := await response.json()) and r_json['uid']
    for field, value in book_creation_data.items():
        assert r_json[field] == value
    assert r_json['available_for_download'] and r_json['available_for_view']


async def test_books_post_failed(
    client: TestClient,
    books_url: str,
    book_creation_data: dict,
    faker: Faker,
) -> None:
    book_creation_data['published_at'] = faker.future_date().isoformat()
    response = await client.post(books_url, json=book_creation_data)
    assert response.status == HTTPBadRequest.status_code
    assert (r_json := await response.json()) and len(r_json) == 1
    assert r_json[0]['loc'] == ['published_at']
    assert r_json[0]['msg'] == 'Date should be in the past'
