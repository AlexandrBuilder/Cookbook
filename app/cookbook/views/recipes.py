from sqlalchemy import func

from aiohttp import web
from aiohttp_apispec import docs, request_schema, response_schema

from app.models.models import Recipe, RecipeStep, RecipeXTag, Tag, User, Image
from app.cookbook.schemas.recipes import RecipeCreateSchema, RecipeSchema, RecipeLifterSchema
from app.utils.response import to_dict, to_dict_list
from app.utils.pagination import pagination
from app.auth.decorators import not_blocked_user
from app.models import db


@docs(
    tags=["recipes"],
    summary="Create new recipe",
    description="Create new recipe",
)
@not_blocked_user
@request_schema(RecipeCreateSchema())
@response_schema(RecipeSchema, 201)
async def recipe_add(request):
    if 'tags' in request['data']:
        tag_names = [tag['name'] for tag in request['data']['tags']]
        tags = await Tag.query.where(Tag.name.in_(tag_names)).gino.all()
        if len(tags) != len(tag_names):
            raise web.HTTPBadRequest(reason='The sequence of tags is non-existent tags')
    else:
        tags = []

    if 'image_id' in request['data']:
        if not await Image.query.where(Image.id == request['data']['image_id']).gino.first():
            raise web.HTTPBadRequest(reason='Image with id={} does not exist'.format(request['data']['image_id']))
        image_id = request['data']['image_id']
    else:
        image_id = None

    recipe = await Recipe.create(
        name=request['data']['name'],
        description=request['data']['description'],
        type=request['data']['type'],
        image_id=image_id,
        user_id=request.user.id
    )
    recipe.user = request.user

    recipe_step_list = [
        {'number': recipe_step['number'], 'description': recipe_step['description'], 'recipe_id': recipe.id}
        for recipe_step in request['data']['recipe_steps']
    ]
    recipe.recipe_steps = await RecipeStep.insert_by_list_data(recipe_step_list)

    tag_list = [{'recipe_id': recipe.id, 'tag_id': tag.id} for tag in tags]
    await RecipeXTag.insert_by_list_data(tag_list)
    recipe.tags = tags

    count_recipe_user = await db.select([func.count(Recipe.id)]).where(Recipe.user_id == request.user.id).gino.scalar()
    await request.user.update(count_recipes=count_recipe_user).apply()

    return web.json_response(to_dict(RecipeSchema, recipe), status=201)


@docs(
    tags=["recipes"],
    summary="View recipe",
    description="View recipe",
)
@not_blocked_user
@response_schema(RecipeSchema, 200)
async def recipe_view(request):
    recipes = await Recipe \
        .outerjoin(User) \
        .outerjoin(RecipeStep) \
        .outerjoin(RecipeXTag) \
        .outerjoin(Tag) \
        .select() \
        .where(Recipe.id == int(request.match_info['id'])) \
        .gino \
        .load(
            Recipe.distinct(Recipe.id)
            .load(add_recipe_step=RecipeStep.distinct(RecipeStep.id))
            .load(add_tag=Tag.distinct(Tag.id))
            .load(user=Tag.distinct(User.id))
        ) \
        .all()

    if not recipes:
        raise web.HTTPNotFound()

    return web.json_response(to_dict(RecipeSchema, recipes[0]))


@docs(
    tags=["recipes"],
    summary="List recipe",
    description="List recipe",
)
@not_blocked_user
@request_schema(RecipeLifterSchema())
@response_schema(RecipeSchema, 200)
async def recipe_list(request):
    query = Recipe \
        .outerjoin(User) \
        .outerjoin(RecipeXTag) \
        .outerjoin(Tag) \
        .select() \
        .where(Recipe.status == Recipe.STATUS_ACTIVE)

    if 'tag' in request['data']:
        if not await Tag.query.where(Tag.name == request['data']['tag']).gino.first():
            raise web.HTTPBadRequest(reason='Tag with name={} does not exist'.format(request['data']['tag']))
        query = query.where(Tag.name == request['data']['tag'])

    if 'name' in request['data']:
        search = "%{}%".format(request['data']['name'])
        query = query.where(Recipe.name.like(search))

    if 'type' in request['data']:
        query = query.where(Recipe.type == request['data']['type'])

    if 'user_id' in request['data']:
        if not await User.query.where(User.id == request['data']['user_id']).gino.first():
            raise web.HTTPBadRequest(reason='User with id={} does not exist'.format(request['data']['user_id']))
        query = query.where(User.id == request['data']['user_id'])

    if 'has_image' in request['data']:
        subquery = Recipe.image_id.isnot(None) if request['data']['has_image'] else Recipe.image_id.is_(None)
        query = query.where(subquery)

    if 'created_sort' in request['data']:
        subquery = Recipe.created.asc() \
            if request['data']['created_sort'] == RecipeLifterSchema.SORT_ASC \
            else Recipe.created.desc()
        query = query.order_by(subquery)

    if 'name_sort' in request['data']:
        subquery = Recipe.name.asc() \
            if request['data']['name_sort'] == RecipeLifterSchema.SORT_ASC \
            else Recipe.name.desc()
        query = query.order_by(subquery)

    if 'count_likes_sort' in request['data']:
        subquery = Recipe.count_likes.asc() \
            if request['data']['count_likes_sort'] == RecipeLifterSchema.SORT_ASC \
            else Recipe.count_likes.desc()
        query = query.order_by(subquery)

    offset, limit = pagination(request['data']['page'], request['data']['per_page'])

    recipes = await query \
        .offset(offset) \
        .limit(limit) \
        .gino \
        .load(
            Recipe.distinct(Recipe.id)
            .load(add_tag=Tag.distinct(Tag.id))
            .load(user=Tag.distinct(User.id))
        ) \
        .all()

    return web.json_response(to_dict_list(RecipeSchema, recipes))
