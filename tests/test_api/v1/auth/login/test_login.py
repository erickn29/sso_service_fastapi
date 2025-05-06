import uuid

from service.auth import AuthService


async def test_login_success(client_admin, init_data):
    response = await client_admin.post(
        "/api/v1/auth/login/",
        json={
            "email": init_data["admin"].email,
            "password": init_data["admin_password"],
        },
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()
    assert isinstance(response.json()["access_token"], str)
    assert isinstance(response.json()["refresh_token"], str)
    assert AuthService().verify_token(response.json()["access_token"])
    assert AuthService().verify_token(response.json()["refresh_token"])


async def test_login_fail_bad_email(client_admin, init_data):
    response = await client_admin.post(
        "/api/v1/auth/login/",
        json={
            "email": init_data["admin"].email + "bad",
            "password": init_data["admin_password"],
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid email or password"


async def test_login_fail_bad_password(client_admin, init_data):
    response = await client_admin.post(
        "/api/v1/auth/login/",
        json={"email": init_data["admin"].email, "password": str(uuid.uuid4())},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid email or password"
