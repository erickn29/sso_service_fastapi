import json

from model import User
from schema.user import UserInputSchema, UserOutputSchema
from service.user import UserServiceV1


async def test_update_user(fake_redis, session, init_data):
    async with session:
        user_obj = await session.get(User, init_data["default"].id)
    assert user_obj.email == init_data["default"].email

    us = UserServiceV1(cache=fake_redis)
    user = await us.update(
        user_id=init_data["default"].id,
        **UserInputSchema(email="em@il.com", password="12345678").model_dump(),
    )
    cached_user = await fake_redis.get(f"user:{user.id}")

    async with session:
        user_obj = await session.get(User, init_data["default"].id)

    assert user.email == "em@il.com"
    assert isinstance(user, UserOutputSchema)
    assert json.loads(cached_user)["email"] == user.email
    assert user_obj.email == user.email
