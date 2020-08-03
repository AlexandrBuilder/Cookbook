from aiohttp import web


async def error_middleware(app, handler):
    async def middleware_handler(request):
        try:
            return await handler(request)
        except web.HTTPException as ex:
            return web.json_response({'error': ex.reason}, status=ex.status)
    return middleware_handler
