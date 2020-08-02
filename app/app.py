import os
import logging
from logging.handlers import RotatingFileHandler
import aioredis

from aiohttp import web
from aiohttp_apispec import setup_aiohttp_apispec, validation_middleware

from config import Config
from app.routes import setup_routes
from app.models import db
from app.core.middlewares.error import error_middleware
from app.auth.middlewares import auth_middleware

try:
    from importlib.metadata import entry_points
except ImportError:
    from importlib_metadata import entry_points


async def on_startup(app):
    app['redis'] = await aioredis.create_redis_pool(app['config'].REDIS_URL)


async def on_cleanup(app):
    app['redis'].close()


async def create_app(dev=True):
    app = web.Application()

    app['config'] = Config
    app['dev'] = dev

    db.init_app(app, {'dsn': Config.DATABASE_URI})

    app.middlewares.append(db)
    app.middlewares.append(error_middleware)
    app.middlewares.append(validation_middleware)
    app.middlewares.append(auth_middleware)

    setup_routes(app)
    setup_aiohttp_apispec(app, swagger_path="/api/docs")

    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_cleanup)

    if not dev:
        if not os.path.exists(Config.LOG_FOLDER):
            os.mkdir(Config.LOG_FOLDER)
        file_handler = RotatingFileHandler(Config.LOG_FILE, maxBytes=10240, backupCount=10)
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

    return app
