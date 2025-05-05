async def test_delete_user_service_201(client_service, init_data):
    response = await client_service.delete(
        f"/api/v1/user/{str(init_data['default'].id)}/"
    )
    assert response.status_code == 201


async def test_delete_user_anonym_401(client_anonym, init_data):
    response = await client_anonym.delete(
        f"/api/v1/user/{str(init_data['default'].id)}/"
    )
    assert response.status_code == 401


async def test_delete_user_blocked_401(client_blocked_service, init_data):
    response = await client_blocked_service.delete(
        f"/api/v1/user/{str(init_data['default'].id)}/"
    )
    assert response.status_code == 401


async def test_delete_user_default_403(client_default, init_data):
    response = await client_default.delete(
        f"/api/v1/user/{str(init_data['default'].id)}/"
    )
    assert response.status_code == 403
