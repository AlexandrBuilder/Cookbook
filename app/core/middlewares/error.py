from aiohttp import web

import traceback


@web.middleware
async def error_middleware(request, handler):
    try:
        response = await handler(request)
        if response.status not in [range(400, 423), 500]:
            return response
        message = response.message
    except web.HTTPException as ex:
        if ex.status not in range(400, 421):
            raise
        message = ex.reason
        status = ex.status
    except Exception as ex:
        status = 500
        message = str(ex) if request.app['dev'] else 'Server error'
        message += ' \n {}'.format(traceback.format_exc())
    return web.json_response({'error': message}, status=status)
