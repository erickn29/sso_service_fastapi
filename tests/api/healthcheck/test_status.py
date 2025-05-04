import uuid

from datetime import datetime

import jwt

from core.config import config
from core.constants import TZ


async def test_healthcheck_admin_200(init_data, fake_redis, client_admin):
    payload_data = {
        "id": str(init_data["admin"].id),
        "expat": datetime.now(tz=TZ.MSK).timestamp() + 300,
    }
    jwt_ = jwt.encode(payload_data, config.app.secret_key, "HS256")
    client_admin.cookies = {"access_token": jwt_}
    response = await client_admin.get("/healthcheck")
    assert response.status_code == 200


async def test_healthcheck_admin_400_expired(init_data, fake_redis, client_admin):
    payload_data = {
        "id": str(init_data["admin"].id),
        "expat": datetime.now(tz=TZ.MSK).timestamp() - 10,
    }
    jwt_ = jwt.encode(payload_data, config.app.secret_key, "HS256")
    client_admin.cookies = {"access_token": jwt_}
    response = await client_admin.get("/healthcheck")
    assert response.status_code == 400
    assert response.text == "Обновите токен"


async def test_healthcheck_admin_400_no_exp(init_data, fake_redis, client_admin):
    payload_data = {
        "id": str(init_data["admin"].id),
        # "expat": datetime.now(tz=TZ.MSK).timestamp() - 10
    }
    jwt_ = jwt.encode(payload_data, config.app.secret_key, "HS256")
    client_admin.cookies = {"access_token": jwt_}
    response = await client_admin.get("/healthcheck")
    assert response.status_code == 400
    assert response.text == "Не найден expat expat"


async def test_healthcheck_admin_400_bad_exp(init_data, fake_redis, client_admin):
    payload_data = {
        "id": str(init_data["admin"].id),
        "expat": str(datetime.now(tz=TZ.MSK)),
    }
    jwt_ = jwt.encode(payload_data, config.app.secret_key, "HS256")
    client_admin.cookies = {"access_token": jwt_}
    response = await client_admin.get("/healthcheck")
    assert response.status_code == 400
    assert response.text == "Неверный формат даты в jwt"


async def test_healthcheck_admin_400_payload_err(init_data, fake_redis, client_admin):
    payload_data = {
        "id": str(init_data["admin"].id),
        "expat": datetime.now(tz=TZ.MSK).timestamp() + 300,
    }
    jwt_ = jwt.encode(payload_data, config.app.secret_key, "HS256")
    jwt_ += "x"
    client_admin.cookies = {"access_token": jwt_}
    response = await client_admin.get("/healthcheck")
    assert response.status_code == 400
    assert response.text == "Ошибка получения token payload"


async def test_healthcheck_admin_400_bad_sing(init_data, fake_redis, client_admin):
    payload_data = {
        "id": str(init_data["admin"].id),
        "expat": datetime.now(tz=TZ.MSK).timestamp() + 300,
    }
    jwt_ = jwt.encode(payload_data, config.app.secret_key + "1", "HS256")
    client_admin.cookies = {"access_token": jwt_}
    response = await client_admin.get("/healthcheck")
    assert response.status_code == 400
    assert response.text == "Ошибка получения token payload"


async def test_healthcheck_service_200(init_data, fake_redis, client_service):
    response = await client_service.get("/healthcheck")
    assert response.status_code == 200


async def test_healthcheck_service_401_bad_key(init_data, fake_redis, client_service):
    client_service.headers = {"x-api-key": str(uuid.uuid4())}
    response = await client_service.get("/healthcheck")
    assert response.status_code == 401
    assert response.json()["detail"] == "Аутентификация не пройдена"


async def test_healthcheck_anonym_401_bad_key(init_data, fake_redis, client_anonym):
    response = await client_anonym.get("/healthcheck")
    assert response.status_code == 401
    assert response.json()["detail"] == "Аутентификация не пройдена"


async def test_healthcheck_blocked_service_401_bad_key(
    init_data, fake_redis, client_blocked_service
):
    response = await client_blocked_service.get("/healthcheck")
    assert response.status_code == 401
    assert response.json()["detail"] == "Пользователь неактивен"
