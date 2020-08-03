import asyncio
import click
from functools import update_wrapper

from config import Config
from app.models.models import User
from app.models import db


def coroutine(f):
    f = asyncio.coroutine(f)

    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(f(*args, **kwargs))

    return update_wrapper(wrapper, f)


@click.group()
@coroutine
async def cli():
    pass


@cli.command()
@click.option('--username', type=str, required=True)
@click.option('--password', type=str, required=True)
@coroutine
async def create_admin(username, password):
    await db.set_bind(Config.DATABASE_URI)
    await db.gino.create_all()

    if await User.query.where(User.username == username).gino.first():
        click.echo(click.style('User "{}" already exist'.format(username), fg="red"))
        return

    user = User(username=username, role=User.ROLE_ADMIN)
    user.set_password(password)

    await user.create()
    await db.pop_bind().close()

    click.echo(click.style('User "{}" with role admin success created'.format(username), fg="green"))


if __name__ == '__main__':
    cli()
