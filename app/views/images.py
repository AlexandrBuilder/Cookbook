from aiohttp import web
from aiohttp_apispec import docs

from app.auth import authorized
from app.schemas.images import ImageSchema
from app.utils import file
from app.models.models import Image
from app.utils.response import to_json


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
@authorized
async def images_add(request):
    data = await request.post()
    image = data['image']
    error = file.validate_extension(image.filename, ['.jpg', '.png'])

    if error:
        raise web.HTTPBadRequest(reason=error)

    filename = file.get_random_filename(image.filename) + file.get_extension(image.filename)
    file.save_file(request.app, filename, image.file)

    image = await Image.create(filename=filename)

    return web.json_response(to_json(ImageSchema, image), status=201)


@docs(
    tags=["images"],
    summary="Get image",
    description="Get image from server",
)
@authorized
async def images_get(request):
    image = await Image.query.where(Image.filename == request.match_info['filename']).gino.first_or_404()
    return web.Response(
        body=file.get_file_content(request.app, image.filename),
        content_type=file.get_image_content_type(image.filename)
    )