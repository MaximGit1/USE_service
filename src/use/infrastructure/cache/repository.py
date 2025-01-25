from typing import cast

from redis.asyncio import Redis

from use.application.cache.protocol import CacheProtocol


class CacheRepository(CacheProtocol):
    def __init__(self, redis_: Redis) -> None:
        self._redis = redis_

    async def get(self, key: str) -> str | None:
        return cast(str | None, await self._redis.get(name=key))

    async def set(self, key: str, value: str, time_: int) -> None:
        await self._redis.setex(
            name=key,
            value=value,
            time=time_,
        )
