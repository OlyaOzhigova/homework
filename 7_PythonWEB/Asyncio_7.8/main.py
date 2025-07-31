import asyncio
from db.migrations import create_tables
from services.data_loader import DataLoader

async def main():
    # создаем таблицы
    await create_tables()
    
    # загружаем данные
    loader = DataLoader()
    await loader.load_all_characters()

if __name__ == '__main__':
    asyncio.run(main())