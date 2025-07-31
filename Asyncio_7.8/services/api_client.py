import aiohttp
from config.settings import settings

class SWAPIClient:
    def __init__(self):
        self.base_url = settings.API_BASE_URL

    async def get_total_records(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url) as response:
                data = await response.json()
                return data.get('total_records', 0)

    async def fetch_character(self, session, character_id):
        url = f"{self.base_url}{character_id}"
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('result', {}).get('properties')
                return None
        except Exception as e:
            print(f"Error fetching character {character_id}: {e}")
            return None