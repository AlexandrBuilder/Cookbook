import asyncio
import click
from functools import update_wrapper

from config import Config
from app.models.models import User
from app.models import db


def coro(f):
    f = asyncio.coroutine(f)

    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(f(*args, **kwargs))

    return update_wrapper(wrapper, f)


@click.group()
@coro
async def cli():
    pass


@cli.command()
@click.option('--username', type=str, required=True)
@click.option('--password', type=str, required=True)
@coro
async def create_admin(username, password):
    await db.set_bind(Config.DATABASE_URI)
    await db.gino.create_all()

    user = User(username=username, role=User.ROLE_ADMIN)
    user.set_password(password)

    await user.create()
    await db.pop_bind().close()

    click.echo('User "{}" with role admin success created'.format(username))


if __name__ == '__main__':
    cli()
