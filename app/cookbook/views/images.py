from aiohttp import web
from aiohttp_apispec import docs, response_schema

from app.auth.decorators import not_blocked_user
from app.cookbook.schemas.images import ImageSchema
from app.utils import file
from app.models.models import Image
from app.utils.response import to_dict


@docs(
    tags=["images"],
    summary="Uploading image",
    description="Uploads a image to the server",
    parameters=[{
        'in': 'body',
        'name': 'image',
        'required': 'true',
    }]
)
@not_blocked_user
@response_schema(ImageSchema, 201)
async def image_add(request):
    data = await request.post()
    image = data['image']
    error = file.validate_extension(image.filename, ['.jpg', '.png'])

    if error:
        raise web.HTTPBadRequest(reason=error)

    filename = file.get_random_filename(image.filename)
    path = file.get_image_path(request.app, filename)
    await file.save_file(path, image.file)

    image = await Image.create(filename=filename)

    return web.json_response(to_dict(ImageSchema, image), status=201)


@docs(
    tags=["images"],
    summary="View image",
    description="View image from server",
)
async def image_view(request):
    image = await Image.query.where(Image.id == int(request.match_info['id'])).gino.first_or_404()
    path = file.get_image_path(request.app, image.filename)
    return web.Response(
        body=await file.get_file_content(path),
        content_type=file.get_image_content_type(path)
    )
