import asyncpg
from utils.config import config
from utils.logger import logger


class Database:
    _pool = None

    @classmethod
    async def connect(cls):
        if cls._pool is None:
            try:
                cls._pool = await asyncpg.create_pool(
                    dsn=config.DATABASE_URL, min_size=1, max_size=5
                )
                logger.info("Connection success")
            except Exception as e:
                logger.error(f"Connection error: {e}")

    @classmethod
    async def disconnect(cls):
        if cls._pool:
            await cls._pool.close()
            cls._pool = None
            logger.info("Database disconnected")

    @classmethod
    async def fetch(cls, query: str, *args):
        async with cls._pool.acquire() as conn:
            logger.info(f"Fetch: {query} | Params: {args}")
            return await conn.fetch(query, *args)

    @classmethod
    async def execute(cls, query: str, *args):
        async with cls._pool.acquire() as conn:
            logger.info(f"Running execution: {query} | Params: {args}")
            return await conn.execute(query, *args)
