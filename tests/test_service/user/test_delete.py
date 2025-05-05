from model import User
from schema.user import UserOutputSchema
from service.user import UserServiceV1


async def test_delete_user(fake_redis, session, init_data):
    async with session:
        user_obj = await session.get(User, init_data["default"].id)
    assert user_obj.is_active is True

    us = UserServiceV1(cache=fake_redis)
    user = await us.delete(user_id=init_data["default"].id)

    async with session:
        user_obj = await session.get(User, init_data["default"].id)

    assert user.is_active == False
    assert isinstance(user, UserOutputSchema)
    assert user_obj.is_active == False
