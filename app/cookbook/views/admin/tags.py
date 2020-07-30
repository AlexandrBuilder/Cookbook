from aiohttp import web
from aiohttp_apispec import docs, request_schema, response_schema

from app.models.models import Tag, User
from app.cookbook.schemas.tags import TagCreateSchema, TagSchema
from app.utils.response import to_dict
from app.auth.decorators import not_blocked_user, has_role


@docs(
    tags=["admin_tags"],
    summary="Create new tag",
    description="Create new tag",
)
@not_blocked_user
@has_role(User.ROLE_ADMIN)
@request_schema(TagCreateSchema())
@response_schema(TagSchema, 201)
async def tag_add(request):
    tag = await Tag.query.where(Tag.name == request['data']['name']).gino.first()
    if tag:
        raise web.HTTPBadRequest(reason='Tag "{}" is already exist'.format(request['data']['name']))
    tag = await Tag.create(name=request['data']['name'])
    return web.json_response(to_dict(TagSchema, tag), status=201)
