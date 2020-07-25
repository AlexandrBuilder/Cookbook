from aiohttp import web
from aiohttp_apispec import docs, request_schema

from app.models.models import User
from app.schemas.schemas import UserRegistrationAndAuthSchema, UserSchema
from app.auth import not_authorized, not_blocked_user
from app.utils.response import to_json, to_json_list


@docs(
    tags=["user"],
    summary="Create new user",
    description="Create new user",
)
@not_authorized
@request_schema(UserRegistrationAndAuthSchema())
async def user_add(request):
    user_by_username = await User.query.where(User.username == request['data']['username']).gino.first()
    if user_by_username:
        raise web.HTTPBadRequest(reason='Username "{}" is already occupied'.format(request['data']['username']))
    user = User(username=request['data']['username'])
    user.set_password(request['data']['password'])
    user = await user.create()
    return web.json_response(to_json(UserSchema, user), status=201)


@docs(
    tags=["user"],
    summary="View user",
    description="View user by username",
)
@not_blocked_user
async def user_view(request):
    user = await User.query.where(User.username == request.match_info['username']).gino.first_or_404()
    return web.json_response(to_json(UserSchema, user))


@docs(
    tags=["user"],
    summary="List users",
    description="List of users added by sorting added recipes",
)
@not_blocked_user
async def user_list(request):
    user = await User.query.where(User.status == User.STATUS_ACTIVE).limit(2).gino.all()
    return web.json_response(to_json_list(UserSchema, user))

