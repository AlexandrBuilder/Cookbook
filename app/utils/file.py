import os
import uuid


def get_random_filename():
    return str(uuid.uuid4())


def get_extension(filename):
    return os.path.splitext(filename)[-1].lower()


def validate_extension(filename, extensions):
    if get_extension(filename) not in extensions:
        return 'The extension must be one of the following: {}'.format(' ,'.join(extensions))


def get_image_path(app, filename):
    return os.path.join(app['config'].UPLOAD_IMAGE_FOLDER, filename)


def save_file(app, filename, file):
    open_file = open(get_image_path(app, filename), 'wb')
    open_file.write(file.read())
    open_file.close()


def get_file_content(app, filename):
    with open(get_image_path(app, filename), 'rb') as open_file:
        bytes = open_file.read()
    return bytes


def get_image_content_type(filename):
    return 'image/{}'.format(get_extension(filename)[1:])
