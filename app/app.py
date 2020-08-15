import logging
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


def setup_log(app):
    logger = logging.getLogger('aiohttp.server')
    handler = logging.FileHandler(app['config'].ERROR_LOG_FILE, mode='a')
    handler.setLevel(logging.ERROR)
    logger.addHandler(handler)


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

    setup_log(app)

    return app
