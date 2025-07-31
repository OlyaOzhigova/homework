import asyncio
import aiohttp

BASE_URL = 'http://localhost:8080/adverts'

async def print_response(response):
    print(f"Status: {response.status}")
    try:
        print("Response:", await response.json())
    except:
        print("Response:", await response.text())
    print()

async def main():
    async with aiohttp.ClientSession() as session:
        print("1. Create advert:")
        async with session.post(BASE_URL, json={
            'title': 'Продам ноутбук',
            'description': 'Отличный ноутбук, почти новый',
            'owner': 'Иван Иванов'
        }) as resp:
            await print_response(resp)
            advert_id = (await resp.json())['id']

        print("2. Get all adverts:")
        async with session.get(BASE_URL) as resp:
            await print_response(resp)

        print("3. Get single advert:")
        async with session.get(f"{BASE_URL}/{advert_id}") as resp:
            await print_response(resp)

        print("4. Update advert:")
        async with session.put(f"{BASE_URL}/{advert_id}", json={
            'title': 'Продам ноутбук (обновлено)',
            'description': 'Отличный ноутбук, почти новый'
        }) as resp:
            await print_response(resp)

        print("5. Delete advert:")
        async with session.delete(f"{BASE_URL}/{advert_id}") as resp:
            await print_response(resp)

        print("6. Verify deletion:")
        async with session.get(f"{BASE_URL}/{advert_id}") as resp:
            await print_response(resp)

if __name__ == '__main__':
    asyncio.run(main())