from aiohttp import web
from aiohttp_apispec import docs, request_schema, response_schema

from app.models.models import User, Recipe
from app.utils.response import to_dict
from app.auth.decorators import not_blocked_user, has_role
from app.cookbook.schemas.recipes import RecipeChangeStatusSchema, RecipeSchema


@docs(
    tags=["admin_recipes"],
    summary="Change recipe status",
    description="Change recipe status",
)
@not_blocked_user
@has_role(User.ROLE_ADMIN)
@request_schema(RecipeChangeStatusSchema())
@response_schema(RecipeSchema, 200)
async def recipe_change_status(request):
    recipe = await Recipe.query.where(Recipe.id == request.match_info['id']).gino.first_or_404()
    if recipe.status == request['data']['status']:
        raise web.HTTPBadRequest(reason='The user already has the status "{}"'.format(request['data']['status']))

    await recipe.update(status=request['data']['status']).apply()

    return web.json_response(to_dict(RecipeSchema, recipe))
