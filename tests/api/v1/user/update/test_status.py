async def test_create_user_service_201(client_service, init_data):
    user_data = {
        "email": "example@email.com",
        "password": "my_password",
        "first_name": "User2",
        "last_name": "User2",
    }
    response = await client_service.put(
        f"/api/v1/user/{str(init_data['default'].id)}/", json=user_data
    )
    assert response.status_code == 201


async def test_create_user_anonym_401(client_anonym, init_data):
    user_data = {
        "email": "example@email.com",
        "password": "my_password",
        "first_name": "User",
        "last_name": "User",
    }
    response = await client_anonym.put(
        f"/api/v1/user/{str(init_data['default'].id)}/", json=user_data
    )
    assert response.status_code == 401


async def test_create_user_blocked_401(client_blocked_service, init_data):
    user_data = {
        "email": "example@email.com",
        "password": "my_password",
        "first_name": "User",
        "last_name": "User",
    }
    response = await client_blocked_service.put(
        f"/api/v1/user/{str(init_data['default'].id)}/", json=user_data
    )
    assert response.status_code == 401


async def test_create_user_default_403(client_default, init_data):
    user_data = {
        "email": "example@email.com",
        "password": "my_password",
        "first_name": "User",
        "last_name": "User",
    }
    response = await client_default.put(
        f"/api/v1/user/{str(init_data['default'].id)}/", json=user_data
    )
    assert response.status_code == 403


async def test_create_user_service_bad_email_422(client_service, init_data):
    user_data = {
        "email": "e@lc",
        "password": "my_password",
        "first_name": "User",
        "last_name": "User",
    }
    response = await client_service.put(
        f"/api/v1/user/{str(init_data['default'].id)}/", json=user_data
    )
    assert response.status_code == 422


async def test_create_user_service_bad_passw_422(client_service, init_data):
    user_data = {
        "email": "example@email.com",
        "password": "my_pa",
        "first_name": "User",
        "last_name": "User",
    }
    response = await client_service.put(
        f"/api/v1/user/{str(init_data['default'].id)}/", json=user_data
    )
    assert response.status_code == 422
