import jwt

from aiohttp import web

from app.models.models import User
from app.auth.jwt import get_jwt_token, get_redis_jwt_key


async def auth_middleware(app, handler):
    async def middleware(request):
        config = app['config']
        request.user = None
        jwt_token = get_jwt_token(request)
        if jwt_token:
            try:
                payload = jwt.decode(jwt_token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM])
            except (jwt.DecodeError, jwt.ExpiredSignatureError):
                raise web.HTTPUnauthorized(reason='Token is invalid')
            redis_jwt_token = await request.app['redis'].execute('get', get_redis_jwt_key(payload['username']))
            if redis_jwt_token and redis_jwt_token == jwt_token:
                raise web.HTTPUnauthorized(reason='Token is invalid')
            request.user = await User.query.where(User.username == payload['username']).gino.first()
        return await handler(request)

    return middleware