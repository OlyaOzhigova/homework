import asyncpg
from config.settings import settings

async def create_tables():
    conn = await asyncpg.connect(
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        database=settings.DB_NAME
    )
    
    try:
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS characters (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                birth_year TEXT,
                eye_color TEXT,
                gender TEXT,
                hair_color TEXT,
                homeworld TEXT,
                mass TEXT,
                skin_color TEXT,
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW()
            )
        ''')
        print("Таблица characters создана успешно")
    finally:
        await conn.close()