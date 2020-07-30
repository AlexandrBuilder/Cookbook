from sqlalchemy import and_

from aiohttp import web
from aiohttp_apispec import docs, request_schema, response_schema

from app.models.models import Recipe, SelectedRecipe
from app.cookbook.schemas.selected_recipes import SelectedRecipeCreateSchema, SelectedRecipeSchema
from app.utils.response import to_dict
from app.auth.decorators import not_blocked_user


@docs(
    tags=["selected_recipes"],
    summary="Create selected recipes",
    description="Create selected recipes",
)
@not_blocked_user
@request_schema(SelectedRecipeCreateSchema())
@response_schema(SelectedRecipeSchema, 201)
async def selected_recipe_add(request):
    if not await Recipe.query.where(Recipe.id == request['data']['recipe_id']).gino.first():
        raise web.HTTPBadRequest(reason='Recipe with id={} does not exist'.format(request['data']['recipe_id']))

    selected_recipe = await SelectedRecipe \
        .query \
        .where(
            and_(SelectedRecipe.recipe_id == request['data']['recipe_id'], SelectedRecipe.user_id == request.user.id)
        ) \
        .gino \
        .first()

    if selected_recipe:
        raise web.HTTPBadRequest(
            reason='SelectedRecipe for a recipe with id={} already exists'.format(request['data']['recipe_id'])
        )

    selected_recipe = await SelectedRecipe.create(recipe_id=request['data']['recipe_id'], user_id=request.user.id)

    return web.json_response(to_dict(SelectedRecipeSchema, selected_recipe), status=201)
