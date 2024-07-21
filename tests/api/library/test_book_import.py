from pathlib import Path

import openpyxl
import pytest
from _pytest.fixtures import SubRequest
from aiohttp import web
from aiohttp.test_utils import TestClient
from aiohttp.web_exceptions import HTTPBadRequest, HTTPOk
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession
from yarl import URL

from app.library.models import Book


@pytest.fixture
def books_import_url(app: web.Application) -> URL:
    return app['library_app'].router['books_import'].url_for()


@pytest.fixture
def file_for_import_with_names(tmp_path: Path, faker: Faker, book_obj: Book) -> Path:
    workbook = openpyxl.Workbook()

    sheet = workbook.active
    sheet.title = 'name'
    data_sheet = [
        ('#', 'name'),
        ('1', book_obj.name),
        ('2', faker.word()),
    ]
    for row_data in data_sheet:
        sheet.append(row_data)

    file_name = tmp_path / f'{faker.pystr()}.xlsx'
    workbook.save(file_name)
    return file_name


@pytest.fixture
def file_for_import_with_authors(tmp_path: Path, faker: Faker, book_obj: Book) -> Path:
    workbook = openpyxl.Workbook()

    sheet = workbook.active
    sheet.title = 'author'
    data_sheet = [
        ('#', 'name'),
        ('1', book_obj.author),
        ('2', faker.word()),
    ]
    for row_data in data_sheet:
        sheet.append(row_data)

    file_name = tmp_path / f'{faker.pystr()}.xlsx'
    workbook.save(file_name)
    return file_name


@pytest.fixture
def file_for_import_invalid_file(tmp_path: Path, faker: Faker) -> Path:
    file_name = tmp_path / f'{faker.pystr()}.csv'
    with file_name.open('w') as f:
        f.write(faker.pystr())
    return file_name


@pytest.fixture(params=['file_for_import_with_names', 'file_for_import_with_authors'])
def file_for_import(request: SubRequest) -> Path:
    return request.getfixturevalue(request.param)


async def test_books_import_file_with_names(
    session: AsyncSession,
    client: TestClient,
    books_import_url: str,
    book_obj: Book,
    file_for_import: Path,
) -> None:
    assert file_for_import.exists()
    assert book_obj.available_for_download

    with file_for_import.open('rb') as f:
        response = await client.post(books_import_url, data={'file': f})
        assert response.status == HTTPOk.status_code

    refreshed_book = await session.get(Book, book_obj.uid)
    assert refreshed_book and not refreshed_book.available_for_download


async def test_books_import_without_file(
    session: AsyncSession,
    client: TestClient,
    books_import_url: str,
    book_obj: Book,
) -> None:
    response = await client.post(books_import_url)
    assert response.status == HTTPBadRequest.status_code
    assert (r_json := await response.json())
    assert r_json['error'] == "AssertionError('multipart/* content type expected')"


async def test_books_import_invalid_file(
    session: AsyncSession,
    client: TestClient,
    books_import_url: str,
    book_obj: Book,
    file_for_import_invalid_file: Path,
) -> None:
    assert file_for_import_invalid_file.exists()

    with file_for_import_invalid_file.open('rb') as f:
        response = await client.post(books_import_url, data={'file': f})
        assert response.status == HTTPBadRequest.status_code
        assert (r_json := await response.json())
        assert r_json['error'] == "BadZipFile('File is not a zip file')"
