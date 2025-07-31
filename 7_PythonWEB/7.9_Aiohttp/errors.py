from aiohttp import web

def json_error(message, status=400, **kwargs):
    return web.json_response({
        "error": message,
        **kwargs
    }, status=status)