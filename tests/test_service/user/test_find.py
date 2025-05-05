import json

from schema.user import UserOutputSchema
from service.user import UserServiceV1


async def test_find_user(fake_redis, session, init_data):
    cached_user = await fake_redis.get(f"user:{init_data["default"].id}")
    assert cached_user is None

    us = UserServiceV1(cache=fake_redis)
    user = await us.find(user_id=init_data["default"].id)
    cached_user = await fake_redis.get(f"user:{user.id}")

    assert isinstance(user, UserOutputSchema)
    assert json.loads(cached_user)["email"] == user.email
