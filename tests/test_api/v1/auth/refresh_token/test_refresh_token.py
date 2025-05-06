from service.auth import AuthService


async def test_refresh_access_token(client_admin, init_data):
    response = await client_admin.post(
        "/api/v1/auth/login/",
        json={
            "email": init_data["admin"].email,
            "password": init_data["admin_password"],
        },
    )
    refresh_token = response.json()["refresh_token"]
    access_token = response.json()["access_token"]

    client_admin.cookies["access_token"] = access_token
    client_admin.cookies["refresh_token"] = refresh_token

    response = await client_admin.get("/api/v1/auth/token/refresh/")
    assert response.status_code == 200

    refresh_token_2 = response.json()["refresh_token"]
    access_token_2 = response.json()["access_token"]

    assert AuthService().verify_token(response.json()["access_token"])
    assert refresh_token_2 == refresh_token
    assert access_token_2 != access_token


async def test_refresh_access_token_no_refresh_in_cookies(client_admin):
    response = await client_admin.get("/api/v1/auth/token/refresh/")
    assert response.status_code == 400
    assert response.json()["detail"] == "Refresh token not found"
