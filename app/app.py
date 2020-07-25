from aiohttp_apispec import setup_aiohttp_apispec, validation_middleware
import aioredis

from aiohttp import web

from config import Config
from app.routes import setup_routes
from app.models import db
from app.error import error_middleware
from app.auth import auth_middleware

try:
    from importlib.metadata import entry_points
except ImportError:  # pragma: no cover
    from importlib_metadata import entry_points


async def create_app(dev=True):
    app = web.Application()
    app['redis'] = await aioredis.create_connection(Config.REDIS_URL)
    app['config'] = Config
    app['dev'] = dev
    db.init_app(app, {'dsn': Config.DATABASE_URI})
    app.middlewares.append(db)
    app.middlewares.append(error_middleware)
    app.middlewares.append(validation_middleware)
    app.middlewares.append(auth_middleware)
    setup_routes(app)
    setup_aiohttp_apispec(app, swagger_path="/api/docs")
    return app
