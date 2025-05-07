from model import User
from service.user import UserServiceV1


async def test_create_user_service_201(client_service, session):
    user_data = {
        "email": "example@email.com",
        "password": "my_password",
        "first_name": "User",
        "last_name": "User",
    }
    response = await client_service.post("/api/v1/user/", json=user_data)
    assert response.status_code == 201

    user = await session.get(User, response.json()["id"])
    assert user.email == "example@email.com"
    assert user.password != "my_password"
    assert UserServiceV1.verify_password("my_password", user.password) is True
    assert user.first_name == "User"
    assert user.last_name == "User"


async def test_create_user_admin_201(client_admin, session):
    user_data = {
        "email": "example@email.com",
        "password": "my_password",
        "first_name": "User",
        "last_name": "User",
    }
    response = await client_admin.post("/api/v1/user/", json=user_data)
    assert response.status_code == 201

    user = await session.get(User, response.json()["id"])
    assert user.email == "example@email.com"
    assert user.password != "my_password"
    assert UserServiceV1.verify_password("my_password", user.password) is True
    assert user.first_name == "User"
    assert user.last_name == "User"


async def test_create_user_anonym_401(client_anonym):
    user_data = {
        "email": "example@email.com",
        "password": "my_password",
        "first_name": "User",
        "last_name": "User",
    }
    response = await client_anonym.post("/api/v1/user/", json=user_data)
    assert response.status_code == 401


async def test_create_user_blocked_401(client_blocked_service):
    user_data = {
        "email": "example@email.com",
        "password": "my_password",
        "first_name": "User",
        "last_name": "User",
    }
    response = await client_blocked_service.post("/api/v1/user/", json=user_data)
    assert response.status_code == 401


async def test_create_user_default_403(client_default):
    user_data = {
        "email": "example@email.com",
        "password": "my_password",
        "first_name": "User",
        "last_name": "User",
    }
    response = await client_default.post("/api/v1/user/", json=user_data)
    assert response.status_code == 403


async def test_create_user_service_bad_email_422(client_service, session):
    user_data = {
        "email": "e@lc",
        "password": "my_password",
        "first_name": "User",
        "last_name": "User",
    }
    response = await client_service.post("/api/v1/user/", json=user_data)
    assert response.status_code == 422


async def test_create_user_service_bad_passw_422(client_service, session):
    user_data = {
        "email": "example@email.com",
        "password": "my_pa",
        "first_name": "User",
        "last_name": "User",
    }
    response = await client_service.post("/api/v1/user/", json=user_data)
    assert response.status_code == 422
