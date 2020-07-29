from aiohttp import web
from aiohttp_apispec import docs, request_schema
from sqlalchemy import func

from app.models.models import Recipe, RecipeStep, RecipeXTag, Tag, User, Image
from app.schemas.recipes import RecipeCreateSchema, RecipeSchema, RecipeLifterSchema
from app.utils.response import to_json, to_json_list
from app.utils.pagination import pagination
from app.auth import not_blocked_user
from app.models import db


@docs(
    tags=["recipes"],
    summary="Create new recipe",
    description="Create new recipe",
)
@not_blocked_user
@request_schema(RecipeCreateSchema())
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

    for recipe_step in request['data']['recipe_steps']:
        recipe_step = await RecipeStep.create(
            number=recipe_step['number'],
            description=recipe_step['description'],
            recipe_id=recipe.id
        )
        recipe.add_recipe_step(recipe_step)

    for tag in tags:
        await RecipeXTag.create(recipe_id=recipe.id, tag_id=tag.id)
        recipe.add_tag(tag)

    count_recipe_user = await db.select([func.count(Recipe.id)]).where(Recipe.user_id == request.user.id).gino.scalar()
    await request.user.update(count_recipe=count_recipe_user).apply()

    return web.json_response(to_json(RecipeSchema, recipe), status=201)


@docs(
    tags=["recipes"],
    summary="View recipe",
    description="View recipe",
)
@not_blocked_user
@request_schema(RecipeCreateSchema())
async def recipe_view(request):
    query = Recipe \
        .outerjoin(User) \
        .outerjoin(RecipeStep) \
        .outerjoin(RecipeXTag) \
        .outerjoin(Tag) \
        .select()

    recipe = await query \
        .where(Recipe.id == int(request.match_info['id'])) \
        .gino \
        .load(Recipe.distinct(Recipe.id).load(add_recipe_step=RecipeStep).load(add_tag=Tag).load(user=User)) \
        .all()

    if not recipe:
        raise web.HTTPNotFound()

    return web.json_response(to_json(RecipeSchema, recipe[0]), status=201)


@docs(
    tags=["recipes"],
    summary="List recipe",
    description="List recipe",
)
@not_blocked_user
@request_schema(RecipeLifterSchema())
async def recipe_list(request):
    query = Recipe \
        .select('id') \
        .select_from(Recipe.outerjoin(User).outerjoin(RecipeXTag).outerjoin(Tag)) \
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

    if 'created' in request['data']:
        query = query.where(func.DATE(Recipe.created) == request['data']['created'])

    offset, limit = pagination(request['data']['page'], request['data']['per_page'])

    recipes = await query.group_by(Recipe.id).offset(offset).limit(limit).gino.all()
    ids = [recipe[0] for recipe in recipes]

    query = Recipe \
        .outerjoin(User) \
        .outerjoin(RecipeXTag) \
        .outerjoin(Tag) \
        .select()

    recipes = await query \
        .where(Recipe.id.in_(ids)) \
        .gino \
        .load(Recipe.distinct(Recipe.id).load(add_tag=Tag).load(user=User)) \
        .all()

    return web.json_response(to_json_list(RecipeSchema, recipes))
