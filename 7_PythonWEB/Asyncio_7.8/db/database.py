import asyncpg
from config.settings import settings

async def get_db_pool():
    return await asyncpg.create_pool(
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        database=settings.DB_NAME,
        min_size=5,
        max_size=20
    )