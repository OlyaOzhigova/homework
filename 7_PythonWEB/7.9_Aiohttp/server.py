from aiohttp import web
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models import Advert, AdvertSchema
from errors import json_error
import datetime
import os

app = web.Application()
engine = create_async_engine("sqlite+aiosqlite:///adverts.db")
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
advert_schema = AdvertSchema()

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Advert.metadata.create_all)

async def get_advert(session, advert_id):
    result = await session.get(Advert, advert_id)
    if not result:
        raise json_error("Advert not found", status=404)
    return result

@web.middleware
async def db_session_middleware(request, handler):
    async with async_session() as session:
        request['session'] = session
        return await handler(request)

app.middlewares.append(db_session_middleware)

async def get_adverts(request):
    session = request['session']
    adverts = (await session.execute(Advert.select())).scalars().all()
    return web.json_response([advert_schema.dump(a) for a in adverts])

async def get_advert_by_id(request):
    advert_id = int(request.match_info['advert_id'])
    session = request['session']
    advert = await get_advert(session, advert_id)
    return web.json_response(advert_schema.dump(advert))

async def create_advert(request):
    session = request['session']
    data = await request.json()
    
    if not all(k in data for k in ['title', 'description', 'owner']):
        raise json_error("Missing required fields", status=400)
    
    advert = Advert(
        title=data['title'],
        description=data['description'],
        owner=data['owner'],
        created_at=datetime.datetime.now()
    )
    session.add(advert)
    await session.commit()
    return web.json_response(advert_schema.dump(advert), status=201)

async def update_advert(request):
    advert_id = int(request.match_info['advert_id'])
    session = request['session']
    data = await request.json()
    
    advert = await get_advert(session, advert_id)
    
    for field in ['title', 'description', 'owner']:
        if field in data:
            setattr(advert, field, data[field])
    
    await session.commit()
    return web.json_response(advert_schema.dump(advert))

async def delete_advert(request):
    advert_id = int(request.match_info['advert_id'])
    session = request['session']
    advert = await get_advert(session, advert_id)
    
    await session.delete(advert)
    await session.commit()
    return web.json_response(status=204)

app.add_routes([
    web.get('/adverts', get_adverts),
    web.get('/adverts/{advert_id}', get_advert_by_id),
    web.post('/adverts', create_advert),
    web.put('/adverts/{advert_id}', update_advert),
    web.delete('/adverts/{advert_id}', delete_advert),
])

async def on_startup(app):
    await init_db()

app.on_startup.append(on_startup)

if __name__ == '__main__':
    web.run_app(app, host=os.getenv('APP_HOST', 'localhost'), 
               port=int(os.getenv('APP_PORT', 8080)))