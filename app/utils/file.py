import mimetypes
import os
import uuid
import aiofiles


def get_extension(filename):
    return os.path.splitext(filename)[-1].lower()


def get_random_filename(filename):
    return str(uuid.uuid4()) + get_extension(filename)


def validate_extension(filename, extensions):
    if get_extension(filename) not in extensions:
        return 'The extension must be one of the following: {}'.format(' ,'.join(extensions))


def get_image_path(app, filename):
    return os.path.join(app['config'].UPLOAD_IMAGE_FOLDER, filename)


async def save_file(path, file):
    async with aiofiles.open(path, 'wb') as open_file:
        await open_file.write(file.read())
        await open_file.flush()


async def get_file_content(path):
    async with aiofiles.open(path, 'rb') as open_file:
        bytes = await open_file.read()
    return bytes


def get_image_content_type(path):
    mimetype, _ = mimetypes.guess_type(path)
    return mimetype
