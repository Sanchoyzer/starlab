import asyncio
from collections.abc import Callable

import pytest
import pytest_asyncio
from aiohttp import web
from aiohttp.test_utils import TestClient
from faker import Faker
from sqlalchemy import delete

from app.library.database import async_session
from app.library.models import Base
from app.main import init_app


@pytest.fixture(scope='session')
def faker() -> Faker:
    return Faker()


@pytest_asyncio.fixture
async def app() -> web.Application:
    return await init_app()


@pytest_asyncio.fixture
async def client(aiohttp_client: Callable, app: web.Application) -> TestClient:
    return await aiohttp_client(app)


@pytest.fixture(scope='session')
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(autouse=True)
async def session():
    async with async_session() as session, session.begin():
        yield session
        for t in Base.metadata.tables.values():
            await session.execute(delete(t))
