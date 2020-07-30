from sqlalchemy import and_, func

from aiohttp import web
from aiohttp_apispec import docs, request_schema, response_schema

from app.models import db
from app.models.models import Recipe, Like
from app.utils.response import to_dict
from app.auth.decorators import not_blocked_user
from app.cookbook.schemas.likes import LikeCreateSchema, LikeSchema


@docs(
    tags=["likes"],
    summary="Create like",
    description="Create like",
)
@not_blocked_user
@request_schema(LikeCreateSchema())
@response_schema(LikeSchema, 201)
async def like_add(request):
    recipe = await Recipe.query.where(Recipe.id == request['data']['recipe_id']).gino.first()
    if not recipe:
        raise web.HTTPBadRequest(reason='Recipe with id={} does not exist'.format(request['data']['recipe_id']))

    like = await Like \
        .query \
        .where(and_(Like.recipe_id == request['data']['recipe_id'], Like.user_id == request.user.id)) \
        .gino \
        .first()

    if like:
        raise web.HTTPBadRequest(
            reason='Like for a recipe with id={} already exists'.format(request['data']['recipe_id'])
        )

    like = await Like.create(recipe_id=request['data']['recipe_id'], user_id=request.user.id)

    recipe_count_likes = await db \
        .select([func.count(Like.id)]) \
        .where(Like.recipe_id == request['data']['recipe_id']) \
        .gino \
        .scalar()
    await recipe.update(count_likes=recipe_count_likes).apply()

    user_count_likes = await db \
        .select([func.sum(Recipe.count_likes)]) \
        .where(Recipe.user_id == request.user.id) \
        .gino \
        .scalar()
    await request.user.update(count_likes=user_count_likes).apply()

    return web.json_response(to_dict(LikeSchema, like), status=201)
