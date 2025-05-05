import uuid

from model import User


async def test_delete_user_service_201(client_service, init_data, session):
    async with session:
        user = await session.get(User, init_data["default"].id)
        assert user.is_active is True

        response = await client_service.delete(
            f"/api/v1/user/{str(init_data['default'].id)}/"
        )
        assert response.json() == {"success": True}

    async with session:
        user = await session.get(User, init_data["default"].id)
        assert user.is_active is False


async def test_delete_user_service_201_false(client_service, init_data):
    response = await client_service.delete(f"/api/v1/user/{str(uuid.uuid4())}/")
    assert response.json() == {"success": False}
