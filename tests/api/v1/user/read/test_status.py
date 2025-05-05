import uuid


async def test_get_user_200(client_service, init_data):
    response = await client_service.get(f"/api/v1/user/{str(init_data['default'].id)}/")
    assert response.status_code == 200


async def test_get_user_404(client_service, init_data):
    response = await client_service.get(f"/api/v1/user/{str(uuid.uuid4())}/")
    assert response.status_code == 404


async def test_get_user_403(client_default, init_data):
    response = await client_default.get(f"/api/v1/user/{str(init_data['default'].id)}/")
    assert response.status_code == 403


async def test_get_user_401(client_anonym, init_data):
    response = await client_anonym.get(f"/api/v1/user/{str(init_data['default'].id)}/")
    assert response.status_code == 401


async def test_get_user_422(client_service, init_data):
    response = await client_service.get("/api/v1/user/123/")
    assert response.status_code == 422
