async def test_create_user_service_201(client_service, session):
    user_data = {
        "email": "example@email.com",
        "password": "my_password",
        "first_name": "User",
        "last_name": "User",
    }
    response = await client_service.post("/api/v1/user/", json=user_data)
    r = response.json()

    assert isinstance(r["id"], str)
    assert r["email"] == user_data["email"]
    assert r["first_name"] == user_data["first_name"]
    assert r["last_name"] == user_data["last_name"]
    assert r["is_active"] is True
    assert r["is_admin"] is False
    assert r["is_service"] is False
    assert isinstance(r["created_at"], str)
    assert isinstance(r["updated_at"], str)
