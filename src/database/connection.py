import asyncpg
from utils.config import config


class Database:
    _pool = None

    @classmethod
    async def connect(cls):
        if cls._pool is None:
            cls._pool = await asyncpg.create_pool(dsn=config.DATABASE_URL, min_size=1, max_size=5)

    @classmethod
    async def disconnect(cls):
        if cls._pool:
            await cls._pool.close()
            cls._pool = None

    @classmethod
    async def fetch(cls, query: str, *args):
        async with cls._pool.acquire() as conn:
            return await conn.fetch(query, *args)

    @classmethod
    async def execute(cls, query: str, *args):
        async with cls._pool.acquire() as conn:
            return await conn.execute(query, *args)
