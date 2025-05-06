import uuid

from model import User
from service.user import UserServiceV1


async def test_verify_email_true(client_default, init_data, fake_redis, session):
    async with session:
        user = await session.get(User, init_data["default"].id)
        assert user.is_verified is False

    token = uuid.uuid4()
    await fake_redis.set(f"verification_token:{token}", str(user.id), ex=60)

    assert await UserServiceV1(cache=fake_redis).verify_email(str(token))

    async with session:
        user = await session.get(User, init_data["default"].id)
        assert user.is_verified is True


async def test_verify_email_false(client_default, init_data, fake_redis, session):
    async with session:
        user = await session.get(User, init_data["default"].id)
        assert user.is_verified is False

    token = uuid.uuid4()
    await fake_redis.set(f"verification_token:{token}", str(user.id), ex=60)

    assert not await UserServiceV1(cache=fake_redis).verify_email(str(uuid.uuid4()))

    async with session:
        user = await session.get(User, init_data["default"].id)
        assert user.is_verified is False
