from aiohttp import web
from aiohttp_apispec import docs, request_schema

from app.models.models import User
from app.auth.schemas.users import UserAuthSchema
from app.auth.jwt import generate_jwt, deactivate_jwt
from app.auth.decorators import not_authorized, authorized


@docs(
    tags=["auth"],
    summary="Authenticated user",
    description="Checks username and password and sends jwt token",
    responses={200: {"accessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...."}}
)
@not_authorized
@request_schema(UserAuthSchema())
async def login(request):
    user = await User.query.where(User.username == request['data']['username']).gino.first()
    if not user or not user.check_password(request['data']['password']):
        raise web.HTTPUnauthorized(reason='Wrong login or password')
    return web.json_response({'accessToken': generate_jwt(request, user)})


@docs(
    tags=["auth"],
    summary="Unauthenticated user",
    description="Deactivating user jwt token",
    responses={200: {"success": "True"}}
)
@authorized
async def logout(request):
    await deactivate_jwt(request)
    return web.json_response({'success': True})
