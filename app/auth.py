import functools
from datetime import datetime, timedelta
import jwt

from aiohttp import web

from app.models.models import User

PREFIX_SCHEMA_BEARER = 'Bearer'


def get_redis_jwt_key(username):
    return 'auth:deactivate:{}'.format(username)


async def deactivate_jwt(request):
    config = request.app['config']
    key = get_redis_jwt_key(request.user.username)
    jwt_token = get_jwt_token(request)
    await request.app['redis'].execute('set', key, jwt_token)
    await request.app['redis'].execute('expire', key, config.JWT_EXP_DELTA_SECONDS)


def generate_jwt(request, user):
    config = request.app['config']
    payload = {
        'username': user.username,
        'exp': datetime.utcnow() + timedelta(seconds=int(config.JWT_EXP_DELTA_SECONDS))
    }
    jwt_token = jwt.encode(payload, config.JWT_SECRET, config.JWT_ALGORITHM)
    return jwt_token.decode('utf-8')


def get_jwt_token(request):
    jwt_token = request.headers.get('authorization', None)
    return jwt_token[(len(PREFIX_SCHEMA_BEARER) + 1):] if jwt_token else None


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


def not_authorized(func):
    @functools.wraps(func)
    def decorated(request, *args, **kwargs):
        if request.user:
            raise web.HTTPForbidden(reason='The method is not available to an authorized user')
        return func(request, *args, **kwargs)

    return decorated


def authorized(func):
    @functools.wraps(func)
    def decorated(request, *args, **kwargs):
        if not request.user:
            raise web.HTTPForbidden(reason='The method is available to an authorized user')
        return func(request, *args, **kwargs)

    return decorated


def has_role(role):
    def _role_required(func):
        @functools.wraps(func)
        def decorated(request, *args, **kwargs):
            if not request.user:
                raise web.HTTPForbidden(reason='The method is available to an authorized user')
            if request.user.role not in role:
                raise web.HTTPForbidden(reason='Not enough rights')
            return func(request, *args, **kwargs)

        return decorated

    return _role_required


def not_blocked_user(func):
    @functools.wraps(func)
    def decorated(request, *args, **kwargs):
        if not request.user:
            raise web.HTTPForbidden(reason='The method is available to an authorized user')
        if request.user.status == User.STATUS_BLOCKED:
            raise web.HTTPForbidden(reason='The user has the status "blocked"')
        return func(request, *args, **kwargs)

    return decorated
