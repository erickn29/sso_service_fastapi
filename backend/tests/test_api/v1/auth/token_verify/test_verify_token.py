async def test_verify_token(client_admin, init_data):
    response = await client_admin.post(
        "/api/v1/auth/login/",
        json={
            "email": init_data["admin"].email,
            "password": init_data["admin_password"],
        },
    )
    refresh_token = response.json()["refresh_token"]
    access_token = response.json()["access_token"]

    response = await client_admin.post(
        "/api/v1/auth/token/verify/", json={"token": access_token}
    )
    assert response.status_code == 200
    assert response.json() == {"is_valid": True}

    response = await client_admin.post(
        "/api/v1/auth/token/verify/", json={"token": refresh_token}
    )
    assert response.status_code == 200
    assert response.json() == {"is_valid": True}
