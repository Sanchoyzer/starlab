from uuid import UUID

import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient
from aiohttp.web_exceptions import HTTPNotFound, HTTPOk
from faker import Faker
from yarl import URL

from app.library.models import Book


@pytest.fixture
def book_url(app: web.Application, book_obj: Book) -> URL:
    return app['library_app'].router['book'].url_for(uid=str(book_obj.uid))


@pytest.fixture
def book_not_exist_url(app: web.Application, book_not_exist_uid) -> URL:
    return app['library_app'].router['book'].url_for(uid=book_not_exist_uid)


@pytest.fixture
def book_not_exist_uid(faker: Faker) -> UUID:
    return faker.uuid4()  # type: ignore[return-value]


async def test_book_get(client: TestClient, book_url: str, book_creation_data: dict) -> None:
    response = await client.get(book_url)
    assert response.status == HTTPOk.status_code
    assert (r_json := await response.json()) and r_json['uid']
    for field, value in book_creation_data.items():
        assert r_json[field] == value
    assert r_json['available_for_download'] and r_json['available_for_view']


async def test_book_get_failed(
    client: TestClient,
    book_not_exist_url: str,
    book_not_exist_uid: UUID,
) -> None:
    response = await client.get(book_not_exist_url)
    assert response.status == HTTPNotFound.status_code
    assert (r_json := await response.json())
    assert r_json == {'error': f"book uid=UUID('{book_not_exist_uid}') not found"}
