import asyncio

import asyncpg
from utils.config import config
from utils.logger import logger


class Database:
    _pool = None

    @classmethod
    async def connect(cls, retries: int = 3, delay: int = 5):
        for attempt in range(retries):
            try:
                cls._pool = await asyncpg.create_pool(
                    dsn=config.DATABASE_URL, min_size=1, max_size=5
                )
                logger.info("Connection success")
                return
            except Exception as e:
                logger.error(f"Connection attempt {attempt + 1} failed: {e}")
                await asyncio.sleep(delay)
        raise ConnectionError(f"Are not able to connect after {retries} retries")

    @classmethod
    async def disconnect(cls) -> None:
        if cls._pool:
            await cls._pool.close()
            cls._pool = None
            logger.info("Database disconnected")

    @classmethod
    async def fetch(cls, query: str, *args):
        try:
            async with cls._pool.acquire() as conn:
                logger.info(f"Fetch: {query} | Params: {args}")
                return await conn.fetch(query, *args)
        except Exception as e:
            logger.error(f"Fetch query error: {e}")
            raise

    @classmethod
    async def execute(cls, query: str, *args):
        try:
            async with cls._pool.acquire() as conn:
                logger.info(f"Running execution: {query} | Params: {args}")
                return await conn.execute(query, *args)
        except Exception as e:
            logger.error(f"Fetch execute error: {e}")
            raise
