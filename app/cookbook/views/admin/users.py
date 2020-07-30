from aiohttp import web
from aiohttp_apispec import docs, request_schema, response_schema

from app.models.models import User
from app.cookbook.schemas.users import UserChangeStatusSchema, UserSchema
from app.auth.decorators import has_role, not_blocked_user
from app.utils.response import to_dict


@docs(
    tags=["admin_users"],
    summary="Change user status",
    description="Change user status",
)
@not_blocked_user
@has_role(User.ROLE_ADMIN)
@request_schema(UserChangeStatusSchema())
@response_schema(UserSchema, 200)
async def user_change_status(request):
    user = await User.query.where(User.username == request.match_info['username']).gino.first_or_404()
    if user.status == request['data']['status']:
        raise web.HTTPBadRequest(reason='The user already has the status "{}"'.format(request['data']['status']))

    await user.update(status=request['data']['status']).apply()

    return web.json_response(to_dict(UserSchema, user))
