from sqlalchemy import and_

from aiohttp import web
from aiohttp_apispec import docs, request_schema, response_schema

from app.models.models import User
from app.cookbook.schemas.users import UserRegistrationSchema, UserSchema
from app.auth.decorators import not_authorized, not_blocked_user
from app.utils.response import to_dict, to_dict_list


@docs(
    tags=["users"],
    summary="Create new user",
    description="Create new user",
)
@not_authorized
@request_schema(UserRegistrationSchema())
@response_schema(UserSchema, 201)
async def user_add(request):
    if await User.query.where(User.username == request['data']['username']).gino.first():
        raise web.HTTPBadRequest(reason='Username "{}" is already occupied'.format(request['data']['username']))

    user = User(username=request['data']['username'])
    user.set_password(request['data']['password'])
    user = await user.create()

    return web.json_response(to_dict(UserSchema, user), status=201)


@docs(
    tags=["users"],
    summary="View user",
    description="View user by username",
)
@not_blocked_user
@response_schema(UserSchema, 200)
async def user_view(request):
    user = await User \
        .query \
        .where(and_(User.username == request.match_info['username'], User.status == User.STATUS_ACTIVE)) \
        .gino \
        .first_or_404()

    return web.json_response(to_dict(UserSchema, user))


@docs(
    tags=["users"],
    summary="List users",
    description="List of users added by sorting added recipes",
)
@not_blocked_user
@response_schema(UserSchema, 200)
async def user_list(request):
    user = await User \
        .query \
        .where(User.status == User.STATUS_ACTIVE) \
        .order_by(User.count_recipe.desc()) \
        .limit(10) \
        .gino \
        .all()

    return web.json_response(to_dict_list(UserSchema, user))
