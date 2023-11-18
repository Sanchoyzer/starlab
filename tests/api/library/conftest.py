from collections.abc import Callable
from datetime import datetime

import pytest
import pytest_asyncio
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from app.library.database import async_session
from app.library.models import Book, GenreType


@pytest.fixture
def factory_book_creation_data(faker: Faker) -> Callable:
    def inner() -> dict:
        return {
            'name': faker.sentence(),
            'author': faker.name(),
            'published_at': faker.past_date(start_date='-200y').isoformat(),
            'genre': faker.enum(GenreType),
            'url': faker.url(),
        }

    return inner


@pytest.fixture
def book_creation_data(factory_book_creation_data: Callable) -> dict:
    return factory_book_creation_data()


def create_book(session: AsyncSession, data: dict) -> Book:
    data['published_at'] = datetime.fromisoformat(data['published_at']).date()
    book = Book(**data)
    session.add(book)
    return book


@pytest_asyncio.fixture
async def book_obj(book_creation_data: dict) -> Book:
    async with async_session() as session, session.begin():
        return create_book(session=session, data=book_creation_data.copy())


@pytest_asyncio.fixture
async def books_list(factory_book_creation_data: Callable, faker: Faker) -> list[Book]:
    async with async_session() as session, session.begin():
        return [
            create_book(session=session, data=factory_book_creation_data())
            for _ in range(faker.pyint(min_value=2, max_value=10))
        ]
