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
    r = response.json()

    assert r["id"] == str(init_data["default"].id)
    assert r["email"] == "example@email.com"
    assert r["first_name"] == "User2"
    assert r["last_name"] == "User2"
    assert r["is_active"] == init_data["default"].is_active
    assert r["is_admin"] == init_data["default"].is_admin
    assert r["is_service"] == init_data["default"].is_service
    assert isinstance(r["created_at"], str)
    assert isinstance(r["updated_at"], str)
