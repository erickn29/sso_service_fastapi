from redis import RedisError
from redis import asyncio as aioredis

from core.config import config
from core.log import logger


class Cache:
    CACHE_TIME = 30

    def __init__(self, redis_url: str, decode_responses: bool = True):
        self.redis_url = redis_url
        self.decode_responses = decode_responses

    @property
    def connection(self):
        return aioredis.from_url(
            self.redis_url,
            encoding="utf-8",
            decode_responses=self.decode_responses,
        )

    async def get(self, name):
        return await self.connection.get(name=name)

    async def ttl(self, name) -> int:
        return await self.connection.ttl(name=name)

    async def exists(self, name) -> bool:
        return bool(await self.connection.exists(name))

    async def set(self, name, value, ex=CACHE_TIME):
        if not isinstance(ex, int) or ex < 1:
            return
        try:
            await self.connection.set(name=name, value=value, ex=ex)
        except RedisError as err:
            logger.error(str(err))

    async def delete(self, key):
        await self.connection.delete(key)

    async def get_keys(self, pattern: str) -> list[str]:
        _, keys = await self.connection.scan(match=pattern)
        return keys

    async def get_many(self, keys: list[str]) -> list:
        return await self.connection.mget(keys=keys)

    async def set_many(self, mapping_data: dict):
        return await self.connection.mset(mapping=mapping_data)

    async def delete_many(self, keys):
        await self.connection.delete(*keys)


cache_service = Cache(redis_url=config.redis.url)
