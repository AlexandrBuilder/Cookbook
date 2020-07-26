from aiohttp import web
from aiohttp_apispec import docs, request_schema

from app.models.models import Recipe, RecipeStep
from app.schemas.recipes import RecipeCreateSchema, RecipeSchema
from app.utils.response import to_json, to_json_list
from app.auth import authorized


@docs(
    tags=["recipes"],
    summary="Create new recipe",
    description="Create new recipe",
)
@authorized
@request_schema(RecipeCreateSchema())
async def recipes_add(request):
    recipe = Recipe(
        name=request['data']['name'],
        description=request['data']['description'],
        type=request['data']['type'],
    )
    recipe.add_user(request.user)
    await recipe.create()
    for recipe_step in request['data']['recipe_steps']:
        recipe_step = await RecipeStep.create(
            number=recipe_step['number'],
            description=recipe_step['description'],
            recipe_id=recipe.id
        )
        recipe.add_recipe_step(recipe_step)

    return web.json_response(to_json(RecipeSchema, recipe), status=201)
