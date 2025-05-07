import json

from model import User
from schema.user import UserInputSchema, UserOutputSchema
from service.user import UserServiceV1


async def test_create_user(fake_redis, session):
    us = UserServiceV1(cache=fake_redis)

    user = await us.create(UserInputSchema(email="em@il.com", password="12345678"))
    cached_user = await fake_redis.get(f"user:{str(user.id)}")
    user_obj = await session.get(User, user.id)

    assert isinstance(user, UserOutputSchema)
    assert json.loads(cached_user)["email"] == user.email
    assert user_obj.email == user.email
