from datetime import datetime, timedelta
import jwt

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
