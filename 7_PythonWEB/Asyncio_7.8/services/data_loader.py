import asyncio
import aiohttp
from db.database import get_db_pool
from services.api_client import SWAPIClient
from config.settings import settings

class DataLoader:
    def __init__(self):
        self.api_client = SWAPIClient()
        self.batch_size = settings.BATCH_SIZE

    async def process_batch(self, session, db_pool, batch_ids):
        tasks = [self.api_client.fetch_character(session, char_id) for char_id in batch_ids]
        characters = await asyncio.gather(*tasks)
        
        valid_chars = []
        for char in characters:
            if char is None:
                continue
            try:
                valid_chars.append({
                    'id': int(char['url'].split('/')[-1]),
                    'name': char.get('name'),
                    'birth_year': char.get('birth_year'),
                    'eye_color': char.get('eye_color'),
                    'gender': char.get('gender'),
                    'hair_color': char.get('hair_color'),
                    'homeworld': char.get('homeworld'),
                    'mass': char.get('mass'),
                    'skin_color': char.get('skin_color')
                })
            except (KeyError, AttributeError) as e:
                print(f"Error processing character data: {e}")
        
        async with db_pool.acquire() as conn:
            await conn.executemany('''
                INSERT INTO characters (
                    id, name, birth_year, eye_color, gender, 
                    hair_color, homeworld, mass, skin_color
                ) VALUES (
                    $1, $2, $3, $4, $5, $6, $7, $8, $9
                ) ON CONFLICT (id) DO UPDATE SET
                    name = EXCLUDED.name,
                    birth_year = EXCLUDED.birth_year,
                    eye_color = EXCLUDED.eye_color,
                    gender = EXCLUDED.gender,
                    hair_color = EXCLUDED.hair_color,
                    homeworld = EXCLUDED.homeworld,
                    mass = EXCLUDED.mass,
                    skin_color = EXCLUDED.skin_color,
                    updated_at = NOW()
            ''', [
                (
                    char['id'], char['name'], char['birth_year'], char['eye_color'],
                    char['gender'], char['hair_color'], char['homeworld'],
                    char['mass'], char['skin_color']
                )
                for char in valid_chars
            ])
        
        print(f"Processed batch {batch_ids[0]}-{batch_ids[-1]}")

    async def load_all_characters(self):
        db_pool = await get_db_pool()
        
        async with aiohttp.ClientSession() as session:
            total = await self.api_client.get_total_records()
            print(f"Total characters to load: {total}")
            
            batch_ranges = range(1, total + 1, self.batch_size)
            for start in batch_ranges:
                end = min(start + self.batch_size - 1, total)
                batch_ids = list(range(start, end + 1))
                await self.process_batch(session, db_pool, batch_ids)
        
        await db_pool.close()