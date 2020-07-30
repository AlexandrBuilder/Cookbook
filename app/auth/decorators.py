import functools

from aiohttp import web

from app.models.models import User


def not_authorized(func):
    @functools.wraps(func)
    def decorated(request, *args, **kwargs):
        if request.user:
            raise web.HTTPForbidden(reason='The method is not available to an authorized user')
        return func(request, *args, **kwargs)

    return decorated


def authorized(func):
    @functools.wraps(func)
    def decorated(request, *args, **kwargs):
        if not request.user:
            raise web.HTTPForbidden(reason='The method is available to an authorized user')
        return func(request, *args, **kwargs)

    return decorated


def has_role(role):
    def _role_required(func):
        @functools.wraps(func)
        def decorated(request, *args, **kwargs):
            if not request.user:
                raise web.HTTPForbidden(reason='The method is available to an authorized user')
            if request.user.role not in role:
                raise web.HTTPForbidden(reason='Permission denied')
            return func(request, *args, **kwargs)

        return decorated

    return _role_required


def not_blocked_user(func):
    @functools.wraps(func)
    def decorated(request, *args, **kwargs):
        if not request.user:
            raise web.HTTPForbidden(reason='The method is available to an authorized user')
        if request.user.status == User.STATUS_BLOCKED:
            raise web.HTTPForbidden(reason='The user has the status "blocked"')
        return func(request, *args, **kwargs)

    return decorated
