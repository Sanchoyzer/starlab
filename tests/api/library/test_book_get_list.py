import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient
from aiohttp.web_exceptions import HTTPOk
from faker import Faker
from yarl import URL

from app.library.models import Book


@pytest.fixture
def books_url(app: web.Application) -> URL:
    return app['library_app'].router['books'].url_for()


@pytest.mark.parametrize('field', ['author', 'name', 'published_at', 'genre'])
async def test_books_get(
    client: TestClient,
    books_url: str,
    books_list: list[Book],
    field: str,
    faker: Faker,
) -> None:
    book = books_list[faker.pyint(max_value=len(books_list) - 1)]

    value = getattr(book, field)
    if field == 'published_at':
        value = value.isoformat()
    value_for_request = value.upper() if field != 'genre' else [value]
    if field in ('author', 'name'):
        val_len = len(value_for_request)
        start = faker.pyint(max_value=2)
        end = faker.pyint(min_value=val_len - 2, max_value=val_len)
        value_for_request = value_for_request[start:end]

    response = await client.get(books_url, params={field: value_for_request})
    assert response.status == HTTPOk.status_code
    assert (r_json := await response.json()) and (items := r_json['items'])

    count_items = len([i for i in books_list if i.genre == value]) if field == 'genre' else 1
    assert len(items) == count_items
    if field == 'genre':
        assert {i['uid'] for i in items} == {str(i.uid) for i in books_list if i.genre == value}
    else:
        assert items[0]['uid'] == str(book.uid)
        assert items[0][field] == value


@pytest.mark.parametrize('field', ['author', 'name'])
async def test_books_get_failed(
    client: TestClient,
    books_url: str,
    books_list: list[Book],
    faker: Faker,
    field: str,
) -> None:
    search_data = {field: faker.word()}
    response = await client.get(books_url, params=search_data)
    assert response.status == HTTPOk.status_code
    assert (r_json := await response.json()) and len(r_json['items']) == 0


async def test_books_get_all(client: TestClient, books_url: str, books_list: list[Book]) -> None:
    response = await client.get(books_url)
    assert response.status == HTTPOk.status_code
    assert (r_json := await response.json()) and (items := r_json['items'])
    assert len(items) == len(books_list)
