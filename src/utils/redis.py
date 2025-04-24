# -*-coding: utf-8 -*-
# @Time    : 2025/4/21 15:42
# @Author  : TyranitarX
from typing import Any
from redis.asyncio import Redis, from_url

REDIS_URI = ""


class RedisClient:
    """A singleton class for a Redis client"""
    _singleton: Redis | None = None

    @classmethod
    async def get_client(cls) -> Redis:
        if cls._singleton is None:
            if not REDIS_URI:
                raise ValueError("REDIS_URI is not set")
            cls._singleton = from_url(REDIS_URI)
        return cls._singleton

    @classmethod
    async def get(cls, key: str):
        client = await cls.get_client()
        value = await client.get(key)
        return value

    @classmethod
    async def set(cls, key: str, value: Any, ttl: int = 300):
        client = await cls.get_client()
        await client.set(key, value, ex=ttl)

    @classmethod
    async def delete(cls, key: str):
        client = await cls.get_client()
        await client.delete(key)

    @classmethod
    async def hget(cls, h: str, key: str):
        client = await cls.get_client()
        value = await client.hget(h, key)
        return value

    @classmethod
    async def hset(cls, h: str, key: str, value: Any):
        client = await cls.get_client()
        await client.hset(h, key, value)


