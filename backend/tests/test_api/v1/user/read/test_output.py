async def test_get_user_200(client_service, init_data):
    response = await client_service.get(f"/api/v1/user/{str(init_data['default'].id)}/")
    r = response.json()

    assert r["id"] == str(init_data["default"].id)
    assert r["email"] == init_data["default"].email
    assert r["first_name"] == init_data["default"].first_name
    assert r["last_name"] == init_data["default"].last_name
    assert r["is_active"] == init_data["default"].is_active
    assert r["is_admin"] == init_data["default"].is_admin
    assert r["is_service"] == init_data["default"].is_service
    assert isinstance(r["created_at"], str)
    assert isinstance(r["updated_at"], str)
