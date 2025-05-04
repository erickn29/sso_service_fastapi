from fakeredis import aioredis


async def get_fake_redis():
    redis = await aioredis.FakeRedis()
    await redis.flushall()
    return redis
