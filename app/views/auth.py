from aiohttp import web
from aiohttp_apispec import docs, request_schema

from app.models.models import User
from app.schemas.schemas import UserRegistrationAndAuthSchema
from app.auth import generate_jwt, not_authorized, authorized, deactivate_jwt


@docs(
    tags=["auth"],
    summary="Authenticated user",
    description="Checks username and password and sends jwt token",
)
@not_authorized
@request_schema(UserRegistrationAndAuthSchema())
async def login(request):
    user = await User.query.where(User.username == request['data']['username']).gino.first()
    if not user or not user.check_password(request['data']['password']):
        raise web.HTTPUnauthorized(reason='Wrong login or password')
    return web.json_response({'accessToken': generate_jwt(request, user)})


@docs(
    tags=["auth"],
    summary="Unauthenticated user",
    description="Deactivating user jwt token",
)
@authorized
async def logout(request):
    await deactivate_jwt(request)
    return web.json_response({'success': True})
