import asyncio

from collections.abc import AsyncGenerator
from typing import Any

import pytest

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
)

from core.config import config
from main import app
from model.base import Base
from tests.helpers.auth.auth import get_jwt
from tests.helpers.cache.cache import get_fake_redis
from tests.helpers.database.database import create_test_database, drop_test_database
from tests.helpers.database.engine import (
    create_engine,
    dispose_engine,
    drop_and_create_tables,
)
from tests.helpers.database.session import get_session
from tests.helpers.http_client.client import get_http_client
from tests.helpers.initial_db_data.data import set_initial_data
from utils.mail import mail_service


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    try:
        loop = asyncio.get_event_loop()
    except (RuntimeError, RuntimeWarning):
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def database():
    db_url = create_test_database(user=config.db.user, password=config.db.password)
    yield db_url
    drop_test_database(db_url)


@pytest.fixture(scope="session")
async def engine(database) -> AsyncGenerator[AsyncEngine, Any]:
    engine = await create_engine(database, Base)
    yield engine
    await dispose_engine(engine)


@pytest.fixture(scope="function", autouse=True)
async def refresh_db(engine):
    await drop_and_create_tables(engine, Base)


@pytest.fixture(scope="function", autouse=True)
async def mock_db_conn_session(mocker, engine):
    session: AsyncSession = await get_session(engine)
    mocker.patch("core.database.db_conn.get_session", return_value=session)


@pytest.fixture(scope="function")
async def session(engine):
    session: AsyncSession = await get_session(engine)
    try:
        yield session
    finally:
        await session.close()


@pytest.fixture(scope="function")
async def init_data(refresh_db, session):
    async with session.begin():
        data = await set_initial_data(session)
    return data


@pytest.fixture
async def fake_redis():
    redis = await get_fake_redis()
    return redis


@pytest.fixture(scope="function", autouse=True)
def mock_send_email(mocker):
    mocker.patch.object(mail_service, "send_email", return_value=None)


@pytest.fixture(scope="function", autouse=True)
async def mock_redis(mocker, fake_redis):
    mocker.patch("core.cache.cache_service", new=fake_redis)


@pytest.fixture(scope="function")
async def client_admin(init_data):
    jwt = get_jwt(init_data["admin"].id, config.app.secret_key)
    client = await get_http_client(app=app, cookies={"access_token": jwt})
    async with client:
        yield client


@pytest.fixture(scope="function")
async def client_default(init_data):
    jwt = get_jwt(init_data["default"].id, config.app.secret_key)
    client = await get_http_client(app=app, cookies={"access_token": jwt})
    async with client:
        yield client


@pytest.fixture(scope="function")
async def client_service(init_data):
    client = await get_http_client(
        app=app, headers={"x-api-key": str(init_data["service"].id)}
    )
    async with client:
        yield client


@pytest.fixture(scope="function")
async def client_blocked_service(init_data):
    client = await get_http_client(
        app=app, headers={"x-api-key": str(init_data["blocked_service"].id)}
    )
    async with client:
        yield client


@pytest.fixture(scope="function")
async def client_anonym():
    client = await get_http_client(app=app)
    async with client:
        yield client
